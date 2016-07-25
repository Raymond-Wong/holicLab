$(document).ready(function() {
  $('#submitBtn').click(function() {
    var gender = $('.radio.checked[name="gender"]').attr('value');
    var role = $('.radio.checked[name="role"]').attr('value');
    post('/user?action=update', {'gender' : gender, 'role' : role}, function(msg) {
      alert('数据录入成功，即将自动跳转');
      setTimeout(function() {
        if (msg != null) {
          window.location.href = '/';
        } else {
          window.location.href = msg;
        }
      }, 1500);
    });
  });
});