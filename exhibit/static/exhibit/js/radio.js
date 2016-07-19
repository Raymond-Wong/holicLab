$(document).ready(function() {
  $('.radio').on('touchend', function() {
    var radioName = $(this).attr('name');
    $('.radio.checked[name="' + radioName + '"]').removeClass('checked');
    $(this).addClass('checked');
  });
})