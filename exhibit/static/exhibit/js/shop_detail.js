$(document).ready(function() {
  carouselInit();
  videoInit();
  initTimepicker();
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

var initTimepicker = function() {
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
    selection.push({'key' : col_1, 'value' : []});
    for (var hoffset = current.getHours(); hoffset < 24; hoffset++) {
      var hour = current.getHours() + '点';
      hour = hour.length == 3 ? hour : '0' + hour;
      var col_2 = (current.getHours() < 12 ? '早上' : '下午') + hour;
      selection[doffset]['value'].push({'key' : col_2, 'value' : []});
      for (var moffset = current.getMinutes(); moffset < 60; moffset += 30) {
        var col_3 = current.getMinutes() + '分';
        col_3 = col_3.length == 3 ? col_3 : '0' + col_3;
        selection[doffset]['value'][selection[doffset]['value'].length - 1]['value'].push({'key' : col_3, 'value' : null});
        current.setMinutes(current.getMinutes() + 30);
      }
    }
  }
  var arg = {
    'col' : 3,
    'colWidth' : [6, 3, 3],
    'selection' : selection,
    'selected' : function(res) {
      console.log(res);
    },
  }
  new MobiSelect($('#bookBtn'), arg);
}