$(document).ready(function() {
  listenCoverType();
  listenBookType();
});

var listenCoverType = function() {
  $('.radio[name="imgOrVideo"]').click(function() {
    var that = $(this);
    if (that.attr('value') == 'image') {
      $('.videoBox').hide()
      $('.imgBox').show();
    } else if (that.attr('value') == 'video') {
      $('.imgBox').hide();
      $('.videoBox').show();
    }
  });
}

var listenBookType = function() {
  $('.radio[name="bookType"]').click(function() {
    if ($(this).attr('value') == 'anytime') {
      $('#timeContainer').hide();
      $('#addTimeBtn').css('visibility', 'hidden');
    } else if ($(this).attr('value') == 'specialTime') {
      $('#timeContainer').show();
      $('#addTimeBtn').css('visibility', 'visible');
    }
  })
}