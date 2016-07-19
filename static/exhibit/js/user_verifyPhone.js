$(document).ready(function() {
  submitAction();
  bindNumberInputCallback(numberInputCallback);
});

var submitAction = function() {
  $('.submitBtn').click(function() {
    var phone = $('input').val();
    var url = '/user?action=verify&type=phone&phone=' + phone;
    post(url, {}, function(msg) {
      var url = '/user?action=verify&type=code';
      window.location.href = url;
    });
  });
}

var numberInputCallback = function(value) {
  // 获取已经输入的所有code
  var codes = $('.codeBox.active');
  var allCodes = $('.codeBox');
  // 如果输入的是回退
  if (value == 'del') {
    var val = $('input').val();
    if (val.length == 0)
      return false;
    val = val.substring(0, val.length - 1);
    $('input').val(val);
  }
  // 如果输入的是确认
  else if (value == 'commit') {
    $('.submitBtn').trigger('click');
  } else {
    // 如果输入的是数字
    var val = $('input').val();
    if (val.length > 11) {
      return false;
    }
    val = val + value;
    $('input').val(val);
  }
}