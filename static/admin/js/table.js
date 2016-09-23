var TABLE = null;

$(document).ready(function() {
  initFilter();
  initMainOption();
  initTable();
  initDatetimepicker();
});

var initFilter = function() {
  initTimeFilter();
  if ($('.filterBox[filter-name="gender"]').length > 0) {
    initGenderFilter();
  }
  if ($('.filterBox[filter-name="role"]').length > 0) {
    initRoleFilter();
  }
  if ($('.filterBox[filter-name="type"]').length > 0) {
    initTypeFilter();
  }

}

var initTimeFilter = function() {
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
}

var initGenderFilter = function() {
  $.fn.dataTable.ext.search.push(
    function( settings, data, dataIndex ) {
      var a = $('.filterBox[filter-name="gender"]').children('.filterValue').val();
      var b = (data[2] == '男性' ? 'male' : 'female');
      if (a == "all" || a == b) {
        return true;
      }
      return false;
    }
  );
  $('.filterBox[filter-name="gender"]').children('.filterValue').click(function() {
    TABLE.draw();
  })
}

var initRoleFilter = function() {
  $.fn.dataTable.ext.search.push(
    function( settings, data, dataIndex ) {
      var a = $('.filterBox[filter-name="role"]').children('.filterValue').val();
      var b = (data[3] == '学生' ? 'student' : 'staff');
      if (a == "all" || a == b) {
        return true;
      }
      return false;
    }
  );
  $('.filterBox[filter-name="role"]').children('.filterValue').click(function() {
    TABLE.draw();
  })
}

var initTypeFilter = function() {
  $.fn.dataTable.ext.search.push(
    function( settings, data, dataIndex ) {
      var a = $('.filterBox[filter-name="type"]').children('.filterValue').val();
      var b = (data[1] == '场地' ? 'site' : 'course');
      if (a == "all" || a == b) {
        return true;
      }
      return false;
    }
  );
  $('.filterBox[filter-name="type"]').children('.filterValue').click(function() {
    TABLE.draw();
  })
}

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
    pageLength: 15
  });
  new $.fn.dataTable.Buttons( TABLE, {
    name: 'commands',
    buttons: ['copy', 'excel']
  });
  debugger;
  TABLE.buttons(0, null).containers().appendTo('.filterWrapper');
  // var tableTools = new $.fn.dataTable.TableTools( TABLE, {
  //   "sSwfPath": "/static/plugin/DataTables/tabletools/swf/copy_csv_xls_pdf.swf",
  //   "buttons": [
  //     "copy",
  //     "excelHtml5",
  //     { "type": "print", "buttonText": "Print me!" }
  //   ],
  // });
  // $('.filterWrapper').append($( tableTools.fnContainer() ));
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