(function ($) {
MobiSelect = function(obj, arg) {
  var col = 1;
  var selections = arg['selection'];
  var selectedCallback = arg['selected'];
  var colWidth = arg['colWidth'];
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
  	if (col != selections.length || colWidth.length != selections.length || col != colWidth.length) {
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
  var iscrollers = [];
  if (this.validateArg(arg)) {
  	var nscontainer = $(selectContainer);
  	var nsSelectBtn = $(nscontainer.find('.selectSubmitBtn')[0]);
  	var nsCancelBtn = $(nscontainer.find('.selectCancelBtn')[0]);
  	$('body').append(nscontainer);
  	for (selectionIndex in selections) {
  	  selection = selections[selectionIndex];
  	  var nswrapper = $(selectWrapper);
  	  nswrapper.css('width', colWidth[selectionIndex] * 100 / 12.0 + '%');
  	  var nslist = $(nswrapper.find('.selectList')[0]);
  	  for (sel in selection) {
  	  	sel = selection[sel];
  	  	nslist.append($(selectItem).html(sel));
  	  }
  	  nscontainer.append(nswrapper);
  	  var iscroll = new IScroll(nswrapper[0], {
	    mouseWheel : true,
	    snap : "li",
	    click : true,
	  });
	  iscrollers.push(iscroll);
  	}
  	if (selectedCallback != undefined) {
  	  nsSelectBtn.click(function() {
  	    var res = [];
  	    for (var i in selections) {
  	      var page = iscrollers[i].currentPage['pageY'];
  	      var val = $($(nscontainer.find('.selectWrapper')[i]).find('li')[page]).html();
  	  	  res.push(val);
  	    }
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
}
})(jQuery);