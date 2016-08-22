var mobiAlert = function(msg, callback) {
  alert(msg);
  var alertBoxContainer = $('#alertBoxContainer');
  var alertBoxText = $(alertBoxContainer.find('.alertText')[0]);
  var alertBtn = $(alertBoxContainer.find('.alertBtn')[0]);
  var alertBtnBox = alertBtn.parent();
  var confirmBtnBox = $(alertBoxContainer.find('.confirmBtn')).parent();
  alertBoxText.text(msg);
  confirmBtnBox.hide();
  alertBtnBox.show();
  alertBoxContainer.show();
  alertBtn.on('tap', function() {
    alertBoxContainer.hide();
    alertBoxText.text('');
    callback();
  });
}

var mobiConfirm = function(msg, callback) {
  var alertBoxContainer = $('#alertBoxContainer');
  var alertBoxText = $(alertBoxContainer.find('.alertText')[0]);
  var alertBtn = $(alertBoxContainer.find('.alertBtn')[0]);
  var alertBtnBox = alertBtn.parent();
  var confirmBtn = $(alertBoxContainer.find('.confirmBtn'))
  var confirmBtnBox = confirmBtn.parent();
  alertBoxText.text(msg);
  alertBtnBox.hide();
  confirmBtnBox.show();
  alertBoxContainer.show();
  confirmBtn.on('tap', function() {
    alertBoxContainer.hide();
    alertBoxText.text('');
    callback($(this).attr('value') == 'true' ? true : false);
  });
}