$(document).ready(function() {
  $('#submitBtn').click(function() {
    var gender = $('.radio.checked[name="gender"]').attr('value');
    var role = $('.radio.checked[name="role"]').attr('value');
    showToast('数据正在录入...');
    post('/user?action=update', {'gender' : gender, 'role' : role}, function(msg) {
      showToast("前往主页中...");
      setTimeout(function() {
        window.location.href = msg;
      }, 1500);
    });
  });
});