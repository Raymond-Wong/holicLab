(function ($) {
MobiSelect = function(obj, arg) {
  var col = 1;
  var selections = arg['selection'];
  var selectedCallback = arg['selected'];
  var colWidth = arg['colWidth'];
  // 检查树的深度
  var valideTreeDeep = function(node, deep) {
    if (node['value'] == null) {
      return (deep == col ? true : false);
    }
    for (var n in node['value']) {
      if (!valideTreeDeep(node['value'][n], deep + 1))
        return false;
    }
    return true;
  }
  // 判断参数是否正确
  this.validateArg = function(arg) {
    // 判断是否绑定对象
    if (obj == undefined || obj == null) {
      throw new Error('binded object cannot be null');
    }
    // 获取列的数量
    if (arg['col'] != undefined) {
      col = arg['col'];
      if (col > 3) {
        throw new Error('max col amount is 3');
      }
    }
    // 判断列的宽度加起来是否是12
    var total = 0;
    for (cw in colWidth) {
      total += colWidth[cw];
    }
    if (total != 12) {
      throw new Error('the sum of col width should be 12');
    }
    // 查看selection树的深度是否和col相等
    var root = {'key' : 'root', 'value' : selections};
    if (!valideTreeDeep(root, 0)) {
      throw new Error("selection is not match with the amount of col");
    }
    return true;
  };
  // animate的隐藏一个container
  var animateHide = function(container) {
    container.animate({'bottom' : '-14em'}, function() {
      $(window).unbind('click');
    })
  };
  // container对象
  var selectContainer = '' + 
  '<div class="selectContainer">' +
    '<div class="selectTopic">' +
      '<font class="selectCancelBtn selectBtn">取消</font>' +
      '选择预约时间' +
      '<font class="selectSubmitBtn selectBtn">确认</font>' +
    '</div>' +
  '</div>';
  // wrapper对象
  var selectWrapper = '' +
    '<div class="selectWrapper">' +
      '<div class="selectScroller">' +
        '<ul class="selectList">' +
        '</ul>' +
      '</div>' +
      '<div class="selectMask">' +
        '<div class="selectMaskUp"></div>' +
        '<div class="selectMaskBottom"></div>' +
      '</div>' +
    '</div>';
  // item对象
  var selectItem = '<li class="selectItem"></li>';
  // 储存所有iscroll对象的数组
  var w2s = {};
  // 当滚动到某个值后需要显示的下一列的wrapper
  var initScroller = function(container, ss, deep, parent) {
    if (ss == null)
      return null;
    var nswrapper = $(selectWrapper).attr('parent', parent).attr('deep', deep).css('width', colWidth[deep] * 100 / 12.0 + '%');
    container.append(nswrapper);
    var nslist = $(nswrapper.find('.selectList')[0]);
    for (sel in ss) {
      var sid = "selectItem_" + deep + '_' + $('.selectWrapper[deep="' + deep + '"]').length + "_" + sel;
      sel = ss[sel];
      nslist.append($(selectItem).html(sel['key']).attr('id', sid));
      initScroller(container, sel['value'], deep + 1, sid);
    }
    var iscroll = new IScroll(nswrapper[0], {
      mouseWheel : true,
      snap : "li",
      click : true,
    });
    w2s[nswrapper.attr('parent')] = iscroll;
    if (deep != 0) {
      nswrapper.addClass('invisible');
    }
    iscroll.on('scrollEnd', function() {
      var wrapper = $(this.wrapper);
      while (wrapper != null && wrapper != undefined && wrapper.length > 0) {
        var nextDeep = parseInt(wrapper.attr('deep')) + 1;
        var listItem = $(wrapper.find('li')[this.currentPage.pageY]);
        wrapper = $('.selectWrapper[parent="' + listItem.attr('id') + '"]');
        $('.selectWrapper[deep="' + nextDeep + '"]').addClass('invisible').removeClass('active');
        if (wrapper.attr('parent') != undefined)
          w2s[wrapper.attr('parent')].goToPage(0, 0);
        wrapper.removeClass('invisible');
        wrapper.addClass('active');
      }
    });
    return nswrapper;
  }
  if (this.validateArg(arg)) {
    var nscontainer = $(selectContainer);
    var nsSelectBtn = $(nscontainer.find('.selectSubmitBtn')[0]);
    var nsCancelBtn = $(nscontainer.find('.selectCancelBtn')[0]);
    $('body').append(nscontainer);
    initScroller(nscontainer, selections, 0, 'root');
    w2s['root'].goToPage(0, 0, 1);
    if (selectedCallback != undefined) {
      nsSelectBtn.click(function() {
        var res = [];
        var page = w2s['root'].currentPage.pageY;
        var val = $($(nscontainer.find('.selectWrapper[deep="0"]')).find('li')[page]).html();
        res.push({'deep' : 0, 'value' : val});
        $.each($(nscontainer.find('.selectWrapper.active')), function() {
          var page = w2s[$(this).attr('parent')].currentPage.pageY;
          var val = $($(this).find('li')[page]).html();
          var deep = $(this).attr('deep');
          res.push({'deep' : deep, 'val' : val});
        });
        selectedCallback(res);
        return false;
      });
    }
    nsCancelBtn.click(function() {
      animateHide(nscontainer);
    });
    obj.click(function() {
      // 把所有selection隐藏
      $('.selectContainer').css('bottom', '-14em');
      nscontainer.animate({'bottom' : "0"}, function() {
        $(window).bind('click', function() {
          animateHide(nscontainer);
        })
      });
    });
  }
}})(jQuery);