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
  $('.playVideoBtn').click(function() {
    var video = $(this).parent().children('video')[0];
    video.play();
  });
}

var str2date = function(str) {
  var date = new Date(str);
  date.setHours(date.getHours() + date.getTimezoneOffset() / 60);
  return date
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
    var col_1 = (doffset == 0 ? '今天' : (current.getMonth() + '月' + current.getDate() + '日 星期' + weeks[current.getDay()]));
    selection.push({'key' : col_1, 'children' : [], 'value' : current.getFullYear() + '-' + current.getMonth() + '-' + current.getDate()});
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
      alert(res);
    },
  }
  new MobiSelect($('#bookBtn'), arg);
}

var initLocationAction = function() {
  wxConfig(['getLocation', 'openLocation']);
  wx.ready(function() {
    console.log('wx is ready');
    wx.getLocation({
        type: 'wgs84', // 默认为wgs84的gps坐标，如果要返回直接给openLocation用的火星坐标，可传入'gcj02'
        success: function (res) {
            var latitude = res.latitude; // 纬度，浮点数，范围为90 ~ -90
            var longitude = res.longitude; // 经度，浮点数，范围为180 ~ -180。
            var speed = res.speed; // 速度，以米/每秒计
            var accuracy = res.accuracy; // 位置精度
            alert(latitude, longitue, speed, accuracy);
        }
    });
  });
}