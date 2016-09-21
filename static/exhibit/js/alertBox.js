var mobiAlert = function(msg, callback) {
  var alertBoxContainer = $('#alertBoxContainer');
  var alertBoxText = $(alertBoxContainer.find('.alertText')[0]);
  var alertBtn = $(alertBoxContainer.find('.alertBtn')[0]);
  var alertBtnBox = alertBtn.parent();
  var confirmBtnBox = $(alertBoxContainer.find('.confirmBtn')).parent();
  alertBoxText.html(msg);
  confirmBtnBox.hide();
  alertBtnBox.show();
  alertBoxContainer.show();
  alertBtn.unbind('tap');
  alertBtn.bind('tap', function(evt) {
    evt.preventDefault();
    alertBoxContainer.hide();
    alertBoxText.html('');
    callback();
    return false;
  });
}

var mobiConfirm = function(msg, callback) {
  var alertBoxContainer = $('#alertBoxContainer');
  var alertBoxText = $(alertBoxContainer.find('.alertText')[0]);
  var alertBtn = $(alertBoxContainer.find('.alertBtn')[0]);
  var alertBtnBox = alertBtn.parent();
  var confirmBtn = $(alertBoxContainer.find('.confirmBtn'))
  var confirmBtnBox = confirmBtn.parent();
  alertBoxText.html(msg);
  alertBtnBox.hide();
  confirmBtnBox.show();
  alertBoxContainer.show();
  confirmBtn.unbind('tap');
  confirmBtn.bind('tap', function() {
    alertBoxContainer.hide();
    alertBoxText.html('');
    callback($(this).attr('value') == 'true' ? true : false);
    return false;
  });
}