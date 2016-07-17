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
  indicator.css('width', slideAmount * 21 - 7 + 'px');
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
  $('.videoBox').click(function() {
    var video = $(this).children('video')[0];
    video.play();
  });
}

var str2date = function(str) {
  var date = new Date(str);
  // date.setHours(date.getHours() + date.getTimezoneOffset() / 60);
  return date
}

var initTimepicker = function() {
  // 获取不可预约时间
  var bookable_times = $.parseJSON($('.shopDetailPage').attr('bookableTimes'));
  var capacity = parseInt($('.shopDetailPage').attr('capacity'));
  $('.shopDetailPage').removeAttr('bookableTimes');
  $('.shopDetailPage').removeAttr('capacity');
  console.log(bookable_times);
  var bookable_time_set = [];
  for (var i in bookable_times) {
    var startTime = str2date(bookable_times[i]['startTime']);
    var endTime = str2date(bookable_times[i]['endTime']);
    var occupation = parseInt(bookable_times[i]['occupation'])
    var bid = bookable_times[i]['id'];
    if (occupation < capacity)
      bookable_time_set.push({'key' : startTime.Format('yyyy-MM-dd hh:mm') + ' ~ ' + endTime.Format('yyyy-MM-dd hh:mm'), 'value' : bid, 'children' : null});
  }
  var selection = bookable_time_set;
  var arg = {
    'col' : 1,
    'colWidth' : [12],
    'selection' : selection,
    'selected' : function(res) {
      alert(res);
    },
  }
  new MobiSelect($('#bookBtn'), arg);
}

var initLocationAction = function() {
  $('.btn.location').bind('click', function() {
    alert('正在初始化地图，请稍后重试');
  });
  wxConfig(['getLocation', 'openLocation']);
  wx.ready(function() {
    $('.btn.location').unbind('click');
    $('.btn.location').click(function() {
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
