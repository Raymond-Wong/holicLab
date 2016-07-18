$(document).ready(function() {
  $('.radio').click(function() {
    var radioName = $(this).attr('name');
    $('.radio.checked[name="' + radioName + '"]').removeClass('checked');
    $(this).addClass('checked');
  });
})