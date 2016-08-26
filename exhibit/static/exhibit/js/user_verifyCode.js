$(document).ready(function() {
  bindNumberInputCallback(numberInputCallback);
});

var numberInputCallback = function(value) {
  // 获取已经输入的所有code
  var codeInput = $('.codeInput')
  // 如果输入的是回退
  if (value == 'del') {
    var code = codeInput.val();
    if (code.length == 0)
      return false;
    code = code.substring(0, code.length - 1);
    codeInput.val(code);
  }
  // 如果输入的是确认
  else if (value == 'commit') {
    var code = codeInput.val();
    if (code.length != 4) {
      mobiAlert('验证码长度不正确');
      return false;
    }
    showToast('核对验证码...');
    post('/user?action=verify&type=code', {'code' : code}, function(msg) {
      if (msg != null) {
        window.location.href = msg;
      } else {
        window.location.href = '/';
      }
    }, function(msg) {
      showToast('验证码错误，请重新输入');
      hideToast(1000);
      codes.removeAttr('value');
      codes.removeClass('active');
    });
  } else {
    // 如果输入的是数字
    var code = codeInput.val();
    // if (code.length >= 4) {
    //   return false;
    // }
    codeInput.val(code + value);
    // 如果当前输入的是第四个数字，则触发提交事件
    if (code.length + 1 >= 4) {
      return numberInputCallback('commit');
    }
  }
}