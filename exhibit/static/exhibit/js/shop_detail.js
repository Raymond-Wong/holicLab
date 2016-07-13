$(document).ready(function() {
  initTimepickerStyle();
  chooseTimeAction();
});

var initTimepickerStyle = function() {
  // $('#timepicker').parent().css('width', '0px');
  // $('#timepicker').parent().css('height', '0px');
  // $('#timepicker').parent().css('margin', '0px');
  // $('#timepicker').parent().css('padding', '0px');
  // $('#timepicker').parent().css('border', '0px');
}

var chooseTimeAction = function() {
  $('#bookBtn').click(function() {
    $('#timepicker').focus();
  });
}