$(document).ready(function() {
  $('.checkBox').on('tap', function() {
    if ($(this).hasClass('checked')) {
      $(this).removeClass('checked');
    } else {
      $(this).addClass('checked');
    }
    return false;
  });
});