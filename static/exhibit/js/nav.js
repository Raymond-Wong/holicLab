$(document).ready(function() {
  $('#getPwdBtn').on('tap', function() {
    showToast('正在获取密码...');
    post('/order?action=password', {}, function(msg) {
      window.location.href = msg;
    }, function(res) {
      setTimeout(function() {
        hideToast();
        alert('asdf' + res['msg']);
      }, 1000);
    });
  });
});