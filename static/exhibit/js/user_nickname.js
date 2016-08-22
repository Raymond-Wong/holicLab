$(document).ready(function() {
  $('#submitBtn').click(function() {
    var nickname = $('input').val();
    post('/user?action=update', {'nickname' : nickname}, function(msg) {
      mobiAlert('数据录入成功，即将自动跳转', function() {
        setTimeout(function() {
          window.location.href = msg;
        }, 1500);
      });
    });
  });
});