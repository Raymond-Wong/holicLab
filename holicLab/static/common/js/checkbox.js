$(document).ready(function() {
  $('.checkBox').on('tap', function() {
    alert('checkbox');
    if ($(this).hasClass('checked')) {
      $(this).removeClass('checked');
    } else {
      $(this).addClass('checked');
    }
    return false;
  });
});