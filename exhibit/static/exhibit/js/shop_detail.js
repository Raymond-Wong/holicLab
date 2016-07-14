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
  var arg = {
    'col' : 3,
    'colWidth' : [6, 3, 3],
    'selection' : [['今天', '7月14日 星期四', '7月15日 星期五'], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5]],
    'selected' : function(res) {
      alert(res);
    },
  }
  new MobiSelect($('#bookBtn'), arg);
}