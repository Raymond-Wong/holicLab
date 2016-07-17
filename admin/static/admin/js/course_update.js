$(document).ready(function() {
  listenCoverType();
  listenBookType();
  addTimeBox();
  deleteTimeBox();
  uploadImage();
  deleteImage();
  submitAction();
  initTimeBtn();
  initCourseUpdate();
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
    // 获取标签
    params['tags'] = $('input[name="tags"]').val();
    // 获取课程时长
    params['duration'] = $('input[name="duration"]').val();
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
    var cid = $('.shopAddWrapper').attr('cid');
    if (cid == undefined || cid == null) {
      topAlert('未明确课程id', 'error');
      return false;
    }
    params['cid'] = cid;
    post('/admin/course?action=update', params, function(msg) {
      topAlert('设置课程信息成功');
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
    var tid = $(this).attr('tid');
    if (endTime < startTime) {
      error = false;
    }
    params['bookable_time'].push({'startTime' : tzAware(startTime), 'endTime' : tzAware(endTime), 'tid' : tid});
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
    var videoLink = $('input[name="videoUrl"]').val();
    var videoCover = $('.videoCover').css('background-image');
    params['cover'].push(videoCover);
    params['cover'].push(videoLink);
    // 检查是否输入了视频地址
    if (params['cover'][1].length <= 0) {
      topAlert('请输入封面视频地址', 'error');
      return false;
    } else if (params['cover'][0].length <= 0) {
      topAlert('请选择封面图片', 'error');
      return false;
    }
  }
  params['cover'] = JSON.stringify(params['cover']);
  return params
}

var initTimeBtn = function() {
  $('.radio[name="bookType"][value="specialTime"]').trigger('click');
}

var initCourseUpdate = function() {
  // 获取商店信息
  var cid = $('.shopAddWrapper').attr('cid');
  post('/admin/course?action=get', {"cid" : cid}, function(msg) {
    var params = $.parseJSON(msg);
    params['cover'] = $.parseJSON(params['cover']);
    // 初始化封面
    if (params['cover_type'] == 'image') {
      for (var i = 0; i < 4; i++) {
        if (i == params['cover'].length)
          break;
        var thumbImg = $($('.imgBox .thumbImg')[i]);
        thumbImg.css('background-image', params['cover'][i]);
        thumbImg.html('<div class="deleteBtn">删除</div>');
        thumbImg.removeClass('uploadImgBtn');
      }
    } else {
      $('.radio[name="imgOrVideo"][value="video"]').trigger('click');
      $('input[name="videoUrl"]').val(params['cover'][1]);
      var thumbImg = $('.videoCover');
      thumbImg.css('background-image', params['cover'][0]);
      thumbImg.html('<div class="deleteBtn">删除</div>');
      thumbImg.removeClass('uploadImgBtn');
    }
    // 初始化课程名称
    $('input[name="name"]').val(params['name']);
    // 初始化课程介绍
    $('textarea[name="description"]').val(params['description']);
    // 初始化教练介绍
    $('textarea[name="coach_description"]').val(params['coach_description']);
    // 初始化教练头像
    $('#coachCover').css('background-image', params['coach_cover']);
    $('#coachCover').html('<div class="deleteBtn">删除</div>');
    $('#coachCover').removeClass('uploadImgBtn');
    // 初始化价格
    $('input[name="price"]').val(parseInt(params['price']));
    // 初始化容量
    $('input[name="capacity"]').val(parseInt(params['capacity']));
    // 初始化标签
    $('input[name="tags"]').val(params['tags']);
    // 初始化注意事项
    $('textarea[name="notice"]').val(params['notice']);
    // 初始化课程时长
    $('input[name="duration"]').val(params['duration']);
    // 初始化可预约时间
    if (params['bookable_time'].length > 0) {
      $('.radio[name="bookType"][value="specialTime"]').trigger('click');
      for (var i = 0; i < params['bookable_time'].length; i++) {
        var period = params['bookable_time'][i];
        var newTimeBox = $(timeBox);
        var startDom = $(newTimeBox.find('input.startTime')[0]);
        var endDom = $(newTimeBox.find('input.endTime')[0]);
        initStartTime(startDom, period['start_time']);
        initEndTime(endDom, period['end_time']);
        newTimeBox.attr('tid', period['id'])
        $('#timeContainer').append(newTimeBox);
      }
    }
  });
}