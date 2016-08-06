$(document).ready(function() {
  $('#getPwdBtn').on('tap', function() {
    post('/order?action=password', {}, function(msg) {
      window.location.href = msg;
    })
  });
});