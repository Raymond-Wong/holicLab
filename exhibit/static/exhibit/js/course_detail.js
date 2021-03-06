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
  return tzAware(date);
}

var initTimepicker = function() {
  // 获取不可预约时间
  var bookable_times = $.parseJSON($('.shopDetailPage').attr('bookableTimes'));
  // 如果没有可预约时间
  if (bookable_times.length == 0) {
    var btn = $('#bookBtn');
    btn.attr('disabled', 'true');
    btn.addClass('disabled');
    btn.text('已结束');
    return false;
  }
  var capacity = parseInt($('.shopDetailPage').attr('capacity'));
  $('.shopDetailPage').removeAttr('bookableTimes');
  $('.shopDetailPage').removeAttr('capacity');
  var bookable_time_set = [];
  for (var i in bookable_times) {
    var startTime = str2date(bookable_times[i]['startTime']);
    var endTime = str2date(bookable_times[i]['endTime']);
    var occupation = parseInt(bookable_times[i]['occupation'])
    var bid = bookable_times[i]['id'];
    if (occupation < capacity)
      bookable_time_set.push({'key' : startTime.Format('MM月dd hh:mm') + ' ~ ' + endTime.Format('MM月dd hh:mm'), 'value' : bid, 'children' : null});
  }
  var selection = bookable_time_set;
  var arg = {
    'col' : 1,
    'colWidth' : [12],
    'selection' : selection,
    'selected' : function(res) {
      var cid = getUrlParam('cid');
      var bid = res[0]
      var url = '/order/pay?action=pre&type=course&cid=' + cid + '&bid=' + bid;
      window.location.href = url;
    },
  }
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
      var shopName = $('.locationBox').attr('shopName');
      getAddressLocation(address, function(result) {
        wx.openLocation({
          latitude: result.location.lat, // 纬度，浮点数，范围为90 ~ -90
          longitude: result.location.lng, // 经度，浮点数，范围为180 ~ -180。
          name: shopName, // 位置名
          address: address, // 地址详情说明
          scale: 15, // 地图缩放级别,整形值,范围从1~28。默认为最大
          infoUrl: '' // 在查看位置界面底部显示的超链接,可点击跳转
        });
      });
    })
  });
}

