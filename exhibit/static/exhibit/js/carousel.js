$(document).ready(function() {
  swipeToScroll();
});

var swipeToScroll = function() {
  $('.carousel').on("swipeleft",function(){
    $(this).carousel('next');
  });
  $('.carousel').on("swiperight",function(){
    $(this).carousel('prev');
  });
}