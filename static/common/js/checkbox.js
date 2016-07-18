$(document).ready(function() {
  $('.checkBox').click(function() {
    if ($(this).hasClass('checked')) {
      $(this).removeClass('checked');
    } else {
      $(this).addClass('checked');
    }
    return false;
  });
});