$(document).ready(function() {
  $('.myLink, a').on('tap', function() {
    if ($(this).hasClass('notMyLink')) {
      return true;
    }
    var link = $(this).attr('href');
    window.location.href = link;
    return false;
  });
});