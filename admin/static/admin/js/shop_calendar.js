$(document).ready(function() {
  initChangeMonthAction();
  initTimeBox();
  deleteTimeBoxAction();
  addTimeBoxAction();
  submitAction();
});

var initTimeBox = function() {
  // 获取商店信息
  var sid = $('.shopAddWrapper').attr('sid');
  post('/admin/shop?action=get', {"sid" : sid}, function(msg) {
    var params = $.parseJSON(msg);
    params['invalide_times'] = $.parseJSON(params['invalide_times']);
    // 初始化不可预约时间
    if (params['invalide_times'].length > 0) {
      for (var i = 0; i < params['invalide_times'].length; i++) {
        var period = params['invalide_times'][i];
        var newTimeBox = $(timeBox);
        var startDom = $(newTimeBox.find('input.startTime')[0]);
        var endDom = $(newTimeBox.find('input.endTime')[0]);
        initStartTime(startDom, period['startTime']);
        initEndTime(endDom, period['endTime']);
        $('#timeContainer').append(newTimeBox);
      }
    }
    updateMonth(new Date());
  });
}

var updateMonth = function(date) {
  var cMonthBox = $('.currentMonthBox');
  var cYear = date.getFullYear();
  var cMonth = date.getMonth() + 1;
  cMonthBox.text(cYear + '年' + cMonth + '月');
  cMonthBox.attr('val', cYear + '-' + cMonth);
  updateTimeBox(date);
}

var deleteTimeBoxAction = function() {
  $(document).delegate('.timeBox .deleteBtn', 'click', function() {
    var stepLine = $(this).parent().parent();
    stepLine.remove();
  })
}

var addTimeBoxAction = function() {
  $('#addTimeBtn').click(function() {
    var newTimeBox = $(timeBox);
    var startDom = $(newTimeBox.find('input.startTime')[0]);
    var endDom = $(newTimeBox.find('input.endTime')[0]);
    initStartTime(startDom, getCurrentMonth());
    initEndTime(endDom);
    $('#timeContainer').append(newTimeBox);
    updateMonth(getCurrentMonth());
  });
}

var getCurrentMonth = function() {
  var cMonthBox = $('.currentMonthBox');
  var cMonthString = cMonthBox.attr('val');
  var cYear = parseInt(cMonthString.split('-')[0]);
  var cMonth = parseInt(cMonthString.split('-')[1]) - 1;
  var cMonthDate = new Date(cYear, cMonth);
  return cMonthDate;
}

var initChangeMonthAction = function() {
  $('.changeMonthBtn').click(function() {
    var cMonthDate = getCurrentMonth();
    var diff = parseInt($(this).attr('diff'));
    cMonthDate.setMonth(cMonthDate.getMonth() + diff);
    updateMonth(cMonthDate);
  });
}

var updateTimeBox = function(month) {
  var hasTime = false;
  $('.noDataLine').hide();
  $('.timeContainer').hide();
  $('.timeContainer .stepLine').hide();
  $('.timeContainer .stepLine').each(function() {
    var timeBox = $(this).children('.timeBox');
    var startTime = timeBox.children('.startTime').datetimepicker('getValue');
    var startTimeYear = startTime.getFullYear();
    var startTimeMonth = startTime.getMonth();
    if (startTimeYear == month.getFullYear() && startTimeMonth == month.getMonth()) {
      hasTime = true
      $(this).show();
    }
  });
  if (!hasTime) {
    $('.noDataLine').show();
  } else {
    $('.timeContainer').show();
  }
}

var submitAction = function() {
  $('#submitBtn').click(function() {
    var params = {};
    params = getBookableTime(params)
    if (params == false) {
      topAlert('所有不可预定时间段中开始时间必须小于等于结束时间', 'error');
      return false;
    }
    // 获取商店id
    var sid = $('.shopAddWrapper').attr('sid');
    params['sid'] = sid;
    console.log(params);
    post('/admin/shop?action=update', params, function(msg) {
      topAlert('更新场地信息成功');
    });
  });
}

var getBookableTime = function(params) {
  params['invalide_times'] = [];
  var error = true;
  $('.timeBox').each(function() {
    var startTime = $(this).children('.startTime').datetimepicker('getValue');
    var endTime = $(this).children('.endTime').datetimepicker('getValue');
    if (endTime < startTime) {
      error = false;
    }
    params['invalide_times'].push({'startTime' : startTime.Format('yyyy-MM-dd hh:mm:ss'), 'endTime' : endTime.Format('yyyy-MM-dd hh:mm:ss')});
  });
  if (!error)
    return error
  params['invalide_times'] = JSON.stringify(params['invalide_times']);
  return params
}