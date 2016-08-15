$(document).ready(function() {
  $('#getPwdBtn').on('tap', function() {
    showToast('正在获取密码...');
    post('/order?action=password', {}, function(msg) {
      hideToast()
      window.location.href = msg;
    })
  });
});