$(document).ready(function() {
  datetimeInit();
  endLargerThanStart();
});

var datetimeInit = function() {
  $.datetimepicker.setLocale('ch');//设置中文
  $('.datetimepicker.endTime').datetimepicker({
    step: 30,
    format: "Y-m-d H:i:00",
  });
  $('.datetimepicker.startTime').datetimepicker({
    step: 30,
    format: "Y-m-d H:i:00",
    onChangeDateTime: endLargerThanStart,
  });
}

var endLargerThanStart = function(db, startDom) {
  if (startDom == undefined)
    return
  var endDom = startDom.parent().children('.endTime');
  var startTime = startDom.datetimepicker('getValue');
  var endTime = endDom.datetimepicker('getValue');
  // 选择一个开始时间后,结束时间选择框在开始时间以前的时间都不允许选择
  endDom.datetimepicker({
    step: 30,
    format: "Y-m-d H:i:00",
    beforeShowDay: function(date) {
      if (date < startTime) {
        return [false, ""]
      }
      return [true, ""];
    }
  });
  // 如果当前结束时间已经小于新的开始时间,则将结束时间设置为开始时间
  if (startTime > endTime) {
    endDom.datetimepicker({
      step: 30,
      format: "Y-m-d H:i:00",
      value: startTime,
      beforeShowDay: function(date) {
        if (date < startTime) {
          return [false, ""]
        }
        return [true, ""];
      }
    })
  }
}