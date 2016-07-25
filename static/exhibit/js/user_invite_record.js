var balance = 0;
var uid = null;

$(document).ready(function() {
  getMetaInfo();
  initRecord();
});

var getMetaInfo = function() {
  var line = $('.infoLine');
  balance = parseInt(line.attr('balance'));
  uid = line.attr('uid');
  line.remove();
}

var initRecord = function() {
  if (balance > 0) {
    $('.stepLine.firstStepLine').removeClass('activeStepLine');
  }
  var stepLines = $('.stepLine');
  for (var i = 0; i < stepLines.length; i++) {
    var stepLine = $(stepLines[i]);
    var val = parseInt(stepLine.attr('value'));
    if (val < balance) {
      stepLine.removeClass('noUseStepLine');
      // 如果当前不是最后一个stepLine
      if (i + 1 < stepLines.length) {
        var nextVal = parseInt($(stepLines[i + 1]).attr('value'));
        if (nextVal > balance) {
          stepLine.addClass('activeStepLine');
          break;
        }
      } else {
        stepLine.addClass('activeStepLine');
      }
    } else if (val == balance) {
      stepLine.removeClass('noUseStepLine');
      stepLine.addClass('activeStepLine');
      break;
    }
  }
}