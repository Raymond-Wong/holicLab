$(document).ready(function() {
  listenCoverType();
  listenBookType();
  addTimeBox();
  deleteTimeBox();
  uploadImage();
  deleteImage();
  submitAction();
  initTimeBtn();
});

var listenCoverType = function() {
  $('.radio[name="imgOrVideo"]').click(function() {
    var that = $(this);
    if (that.attr('value') == 'image') {
      $('.videoBox').hide()
      $('.imgBox').show();
    } else if (that.attr('value') == 'video') {
      $('.imgBox').hide();
      $('.videoBox').show();
    }
  });
}

var listenBookType = function() {
  $('.radio[name="bookType"]').click(function() {
    if ($(this).attr('value') == 'anytime') {
      $('#timeContainer').hide();
      $('#addTimeBtn').css('visibility', 'hidden');
    } else if ($(this).attr('value') == 'specialTime') {
      $('#timeContainer').show();
      $('#addTimeBtn').css('visibility', 'visible');
    }
  })
}

var addTimeBox = function() {
  $('#addTimeBtn').click(function() {
    var newTimeBox = $(timeBox);
    var startDom = $(newTimeBox.find('input.startTime')[0]);
    var endDom = $(newTimeBox.find('input.endTime')[0]);
    initStartTime(startDom);
    initEndTime(endDom);
    $('#timeContainer').append(newTimeBox);
  });
}

var deleteTimeBox = function() {
  $(document).delegate('.timeBox .deleteBtn', 'click', function() {
    var stepLine = $(this).parent().parent();
    stepLine.remove();
  })
}

var uploadImage = function() {
  var inputStr = '<input type="file" name="image" multiple="multiple" accept="image/*" class="hide" />';
  $(document).delegate('.uploadImgBtn', 'click', function() {
    var inputDom = $(inputStr);
    $('body').append(inputDom);
    autoUpload(inputDom, $(this));
  });
}

var autoUpload = function(dom, btn) {
  dom.trigger('click');
  var url = '/admin/upload';
  dom.fileupload({
    autoUpload: true,//是否自动上传
    url: url,//上传地址
    sequentialUploads: true,
    add: function (e, data) {
      btn.removeClass('uploadImgBtn');
      btn.html('<font class="vertical_inner">正在上传中...</font>');
      data.submit();
    },
    done: function (e, resp) {
      resp = resp['result'];
      if (resp['code'] != 0) {
        btn.addClass('uploadImgBtn');
        btn.html('<font class="vertical_inner glyphicon glyphicon-plus"></font>');
        topAlert(resp['msg'], 'error');
      } else {
        btn.html('<div class="deleteBtn">删除</div>');
        btn.css('background-image', 'url(' + resp['msg'] + ')')
      }
      $(this).remove();
    },
  });
}

var deleteImage = function() {
  $(document).delegate('.thumbImg .deleteBtn', 'click', function() {
    var thumbImg = $(this).parent();
    thumbImg.css('background-image', 'url()');
    thumbImg.html('<font class="vertical_inner glyphicon glyphicon-plus"></font>');
    thumbImg.addClass('uploadImgBtn');
  });
}

var submitAction = function() {
  $('#submitBtn').click(function() {
    var params = {};
    // 获取场地名称
    params['name'] = $('input[name="name"]').val();
    if (params['name'].length <= 0) {
      topAlert('请填写课程名称', 'error');
      return false;
    } else if (params['name'].length > 50) {
      topAlert('课程名称不得超过50字', 'error');
      return false;
    }
    // 获取封面类型以及内容
    params = getCoverMedia(params)
    if (params == false)
      return false;
    // 获取描述
    params['description'] = $('textarea[name="description"]').val();
    if (params['description'].length <= 0) {
      topAlert('请填写课程介绍', 'error');
      return false;
    }
    // 获取地址
    params['coach_description'] = $('textarea[name="coach_description"]').val();
    if (params['coach_description'].length <= 0) {
      topAlert('请填写教练简介', 'error')
      return false;
    }
    // 获取教练头像
    params['coach_cover'] = $('#coachCover').css('background-image');
    // 获取价格
    params['price'] = $('input[name="price"]').val();
    // 获取容量
    params['capacity'] = $('input[name="capacity"]').val();
    // 获取注意事项
    params['notice'] = $('textarea[name="notice"]').val();
    if (params['notice'].length <= 0) {
      topAlert('请填写注意事项', 'error');
      return false;
    }
    // 获取可预约时间
    params = getBookableTime(params);
    if (params == false) {
      topAlert('所有不可预定时间段中开始时间必须小于等于结束时间', 'error');
      return false;
    }
    // 获取商店id
    var sid = $('.shopAddWrapper').attr('sid');
    if (sid == undefined || sid == null) {
      topAlert('未明确课程所属场地', 'error');
      return false;
    }
    post('/admin/course?action=add&sid=' + sid, params, function(msg) {
      topAlert('创建课程成功');
    });
  })
}

var getBookableTime = function(params) {
  params['bookable_time'] = [];
  var error = true;
  if ($('.radio.checked[name="bookType"]').attr('value') == 'anytime') {
    return params;
  }
  $('.timeBox').each(function() {
    var startTime = $(this).children('.startTime').datetimepicker('getValue');
    var endTime = $(this).children('.endTime').datetimepicker('getValue');
    if (endTime < startTime) {
      error = false;
    }
    params['bookable_time'].push({'startTime' : startTime, 'endTime' : endTime});
  });
  if (!error)
    return error
  params['bookable_time'] = JSON.stringify(params['bookable_time']);
  return params
}

var getCoverMedia = function(params) {
  // 获取封面类型
  params['cover_type'] = $('.radio.checked').attr('value');
  // 获取封面内容
  if (params['cover_type'] == 'image') {
    params['cover'] = []
    $('.imgBox .thumbImg').each(function() {
      var imgUrl = $(this).css('background-image');
      imgUrl = imgUrl.replace('url(', '');
      if (imgUrl[imgUrl.length - 1] == ')') {
        imgUrl = imgUrl.substring(0, imgUrl.length - 1);
      }
      if (imgUrl.length > 0 && imgUrl != 'none')
        params['cover'].push($(this).css('background-image'));
    });
    // 检查是否至少上传一张封面图
    if (params['cover'].length <= 0) {
      topAlert('请至少上传一张封面图', 'error');
      return false;
    }
  } else if (params['cover_type'] == 'video') {
    params['cover'] = $('input[name="videoUrl"]').val();
    // 检查是否输入了视频地址
    if (params['cover'].length <= 0) {
      topAlert('请输入封面视频地址', 'error');
      return false;
    }
  }
  params['cover'] = JSON.stringify(params['cover']);
  return params
}

var initTimeBtn = function() {
  $('.radio[name="bookType"][value="specialTime"]').trigger('click');
}