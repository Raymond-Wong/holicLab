var TABLE = null;

$(document).ready(function() {
  $.fn.dataTable.ext.search.push(
    function( settings, data, dataIndex ) {
      var startTime = $('.filterValue[name="startDate"]').val();
      var endTime = $('.filterValue[name="endDate"]').val();
      var time = data[0];
      if ((startTime.length == 0 || largerOrEqual(time, startTime)) &&
          (endTime.length == 0 || !largerOrEqual(time, endTime))) {
        return true;
      }
      return false;
    }
  );
  initMainOption();
  initTable();
  initDatetimepicker();
});

var initMainOption = function() {
  var type = getUrlParam('state');
  if (!(type == undefined || type.length == 0 || type == null)) {
    $('.mainOptionBtn.active').removeClass('active');
    $('.mainOptionBtn[state="' + type + '"]').addClass('active');
  }
}


var largerOrEqual = function(timeA, timeB) {
  timeA = timeA.split('-');
  timeB = timeB.split('-');
  if (parseInt(timeB[0]) > parseInt(timeA[0]))
    return false;
  if (parseInt(timeB[0]) == parseInt(timeA[0]) &&
      parseInt(timeB[1]) > parseInt(timeA[1]))
    return false
  if (parseInt(timeB[0]) == parseInt(timeA[0]) &&
      parseInt(timeB[1]) == parseInt(timeA[1]) &&
      parseInt(timeB[2]) > parseInt(timeA[2]))
    return false
  return true;
}

var initTable = function() {
  TABLE = $('#memberTable').DataTable({
    autoWidth : false,
    lengthChange: false,
    pageLength: 15,
  });
}

var initDatetimepicker = function() {
  $('.filterValue[name="startDate"]').datetimepicker({
    lang:'ch',
    timepicker:false,
    format:'Y-m-d',
    onChangeDateTime: endLargerThanStart,
  });
  $('.filterValue[name="endDate"]').datetimepicker({
    lang:'ch',
    timepicker:false,
    format:'Y-m-d',
    onChangeDateTime: filterTime,
  });
}

var endLargerThanStart = function() {
  var startTime = $('.filterValue[name="startDate"]').datetimepicker('getValue');
  var endTime = $('.filterValue[name="endDate"]').datetimepicker('getValue');
  $('.filterValue[name="endDate"]').datetimepicker({
    lang: 'ch',
    timepicker: false,
    format: 'Y-m-d',
    value: startTime == null ? null : (startTime > endTime ? startTime : endTime),
    onChangeDateTime: filterTime,
    beforeShowDay: function(date) {
      if (startTime == null)
        return true;
      if ((date.getYear() < startTime.getYear()) ||
          (date.getYear() == startTime.getYear() && date.getMonth() < startTime.getMonth()) ||
          (date.getYear() == startTime.getYear() && date.getMonth() == startTime.getMonth() && date.getDate() < startTime.getDate())) {
        return [false, ""]
      }
      return [true, ""];
    }
  });
  filterTime();
}

var filterTime = function() {
  TABLE.draw();
}