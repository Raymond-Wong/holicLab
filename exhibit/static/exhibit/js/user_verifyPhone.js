$(document).ready(function() {
  $('.submitBtn').click(function() {
    var phone = $('input').val();
    var url = '/user?action=verify&type=phone&phone=' + phone;
    post(url, {}, function(msg) {
      var url = '/user?action=verify&type=code';
      window.location.href = url;
    });
  });
});