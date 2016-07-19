$(document).ready(function() {
  $('.radio').on('touchstart', function() {
    var radioName = $(this).attr('name');
    $('.radio.checked[name="' + radioName + '"]').removeClass('checked');
    $(this).addClass('checked');
  });
})