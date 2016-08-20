$(document).ready(function() {
  bindNumberInputCallback(numberInputCallback);
});

var numberInputCallback = function(value) {
  // 获取已经输入的所有code
  var codes = $('.codeBox.active');
  var allCodes = $('.codeBox');
  // 如果输入的是回退
  if (value == 'del') {
    if (codes.length == 0)
      return false;
    var target = $(codes[codes.length - 1]);
    target.removeAttr('value');
    target.removeClass('active');
  }
  // 如果输入的是确认
  else if (value == 'commit') {
    if (codes.length != 4) {
      return false;
    }
    var code = '';
    codes.each(function() {
      code += $(this).attr('value');
    });
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
    });
  } else {
    // 如果输入的是数字
    if (codes.length == 4) {
      return false;
    }
    $(allCodes[codes.length]).addClass('active').attr('value', value);
    // 如果当前输入的是第四个数字，则触发提交事件
    if (codes.length + 1 >= 4) {
      return numberInputCallback('commit');
    }
  }
}