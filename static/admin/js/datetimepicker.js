$(document).ready(function() {
  datetimeInit();
  endLargerThanStart();
});

var datetimeInit = function() {
  $.datetimepicker.setLocale('ch');//设置中文
  initEndTime($('.datetimepicker.endTime'));
  initStartTime($('.datetimepicker.startTime'));
}

var initEndTime = function(doms, defaultTime) {
  doms.datetimepicker({
    step: 30,
    format: "Y-m-d H:i:00",
    value: defaultTime,
  });
}

var initStartTime = function(doms, defaultTime) {
  doms.datetimepicker({
    step: 30,
    format: "Y-m-d H:i:00",
    value: defaultTime,
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
      if ((date.getYear() < startTime.getYear()) ||
          (date.getYear() == startTime.getYear() && date.getMonth() < startTime.getMonth()) ||
          (date.getYear() == startTime.getYear() && date.getMonth() == startTime.getMonth() && date.getDate() < startTime.getDate())) {
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
        if ((date.getYear() < startTime.getYear()) ||
            (date.getYear() == startTime.getYear() && date.getMonth() < startTime.getMonth()) ||
            (date.getYear() == startTime.getYear() && date.getMonth() == startTime.getMonth() && date.getDate() < startTime.getDate())) {
          return [false, ""]
        }
        return [true, ""];
      }
    })
  }
}