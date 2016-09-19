$(document).ready(function() {
  carouselInit();
  videoInit();
  initTimepicker();
  initLocationAction();
});

var carouselInit = function() {
  if ($('#wrapper').length == 0)
    return false;
  var scroller = $('#scroller');
  var indicator = $('#indicator');
  var slideAmount = scroller.find('.slide').length;
  scroller.css('width', slideAmount * 100 + 'vw');
  indicator.css('width', slideAmount * 15 - 5 + 'px');
  myScroll = new IScroll('#wrapper', {
    scrollX: true,
    scrollY: false,
    momentum: false,
    snap: true,
    snapSpeed: 400,
    keyBindings: true,
    indicators: {
      el: document.getElementById('indicator'),
      resize: false
    }
  });
}

var videoInit = function() {
  if ($('.videoBox').length == 0)
    return false;
  $('.videoBox').on('tap', function() {
    var video = $(this).children('video')[0];
    video.play();
  });
}

var str2date = function(str) {
  var left = str.split(' ')[0];
  var right = str.split(' ')[1];
  var leftArr = left.split('-');
  var rightArr = right.split(':');
  var date = new Date(leftArr[0], parseInt(leftArr[1])- 1, leftArr[2], rightArr[0], rightArr[1]);
  return date;
}

var initTimepicker = function() {
  // 获取不可预约时间
  var invalide_times = $.parseJSON($('.shopDetailPage').attr('invalideTimes'));
  $('.shopDetailPage').removeAttr('invalideTimes');
  var invalide_times_set = [];
  for (var i in invalide_times) {
    var startTime = str2date(invalide_times[i]['startTime']);
    var endTime = str2date(invalide_times[i]['endTime']);
    for (; startTime < endTime; startTime.setMinutes(startTime.getMinutes() + 30)) {
      invalide_times_set.push(startTime.Format('yyyy-MM-dd hh:mm'));
    }
  }
  var selection = [];
  var now = new Date();
  // 把当前时间变成最近的一个整30分钟
  now.setSeconds(0);
  if (now.getMinutes() > 30) {
    now.setMinutes(0);
    now.setHours(now.getHours() + 1);
  } else if (now.getMinutes() > 0) {
    now.setMinutes(30);
  }
  var weeks = ['日', '一', '二', '三', '四', '五', '六'];
  var current = new Date(now);
  for (var doffset = 0; doffset < 3; doffset++) {
    var col_1 = (doffset == 0 ? '今天' : (current.getMonth() + 1 + '月' + current.getDate() + '日 星期' + weeks[current.getDay()]));
    selection.push({'key' : col_1, 'children' : [], 'value' : current.getFullYear() + '-' + (current.getMonth() + 1) + '-' + current.getDate()});
    for (var hoffset = current.getHours(); hoffset < 24; hoffset++) {
      var hour = current.getHours() + '点';
      hour = hour.length == 3 ? hour : '0' + hour;
      var col_2 = (current.getHours() < 12 ? '早上' : '下午') + hour;
      selection[selection.length - 1]['children'].push({'key' : col_2, 'children' : [], 'value' : current.getHours()});
      for (var moffset = current.getMinutes(); moffset < 60; moffset += 30) {
        var col_3 = current.getMinutes() + '分';
        col_3 = col_3.length == 3 ? col_3 : '0' + col_3;
        if ($.inArray(current.Format('yyyy-MM-dd hh:mm'), invalide_times_set) < 0) {
          selection[selection.length - 1]['children'][selection[selection.length - 1]['children'].length - 1]['children'].push({'key' : col_3, 'children' : null, 'value' : current.getMinutes()});
        }
        current.setMinutes(current.getMinutes() + 30);
      }
      if (selection[selection.length - 1]['children'][selection[selection.length - 1]['children'].length - 1]['children'].length == 0) {
        selection[selection.length - 1]['children'].pop();
      }
    }
    if (selection[selection.length - 1]['children'].length == 0) {
      selection.pop();
    }
  }
  var arg = {
    'col' : 3,
    'colWidth' : [6, 3, 3],
    'selection' : selection,
    'selected' : function(res) {
      var sid = getUrlParam('sid');
      var dateArr = res[0].split('-');
      var newDate = new Date(dateArr[0], parseInt(dateArr[1]) - 1, dateArr[2], res[1], res[2]);
      var timestamp = newDate.valueOf() / 1000;
      var url = '/order/pay?action=pre&type=site&sid=' + sid + '&timestamp=' + timestamp;
      window.location.href = url;
    },
  }
  alert(selection.length);
  new MobiSelect($('#bookBtn'), arg);
}

var initLocationAction = function() {
  $('.btn.location').bind('tap', function() {
    mobiAlert('正在初始化地图，请稍后重试');
  });
  wxConfig(['getLocation', 'openLocation']);
  wx.ready(function() {
    $('.btn.location').unbind('tap');
    $('.btn.location').on('tap', function() {
      var address = $('.locationBox').text();
      getAddressLocation(address, function(result) {
        wx.openLocation({
          latitude: result.location.lat, // 纬度，浮点数，范围为90 ~ -90
          longitude: result.location.lng, // 经度，浮点数，范围为180 ~ -180。
          name: '全能工作室', // 位置名
          address: '深圳市宝安中心新安六路与宝源南路交界处众里创业社区首层', // 地址详情说明
          scale: 15, // 地图缩放级别,整形值,范围从1~28。默认为最大
          infoUrl: '' // 在查看位置界面底部显示的超链接,可点击跳转
        });
      });
    })
  });
}

