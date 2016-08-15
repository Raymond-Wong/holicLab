var showToast = function(msg) {
  if (msg == null || msg == undefined) {
    msg = $('.toastText').text();
  }
  $('.toastText').text(msg);
  $('.toastContainer').show();
}

var hideToast = function(seconds) {
  if (seconds == undefined || seconds == null) {
    $('.toastContainer').hide();
  } else {
    setTimeout(function() {
      $('.toastContainer').hide();
    }, seconds);
  }
}