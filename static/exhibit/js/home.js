$(document).ready(function() {
  $('.courseWrapper').each(function() {
    new IScroll(this, { scrollX: true, scrollY: false, mouseWheel: true, eventPassthrough: true});
  });
})