$(document).ready(function() {
  listenCoverType();
  listenBookType();
  addTimeBox();
  deleteTimeBox();
  uploadImage();
  deleteImage();
  submitAction();
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
  $(document).delegate('.imgBox .thumbImg .deleteBtn', 'click', function() {
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
      topAlert('请填写场地名称', 'error');
      return false;
    } else if (params['name'].length > 50) {
      topAlert('场地名称不得超过50字', 'error');
      return false;
    }
    // 获取封面类型以及内容
    params = getCoverMedia(params)
    if (params == false)
      return false;
    // 获取描述
    params['description'] = dumpsNewline($('textarea[name="description"]').val());
    if (params['description'].length <= 0) {
      topAlert('请填写场地介绍', 'error');
      return false;
    }
    // 获取地址
    params['location'] = $('input[name="location"]').val();
    if (params['location'].length <= 0) {
      topAlert('请填写场地地址', 'error');
      return false;
    } else if (params['location'].length > 200) {
      topAlert('场地地址不得超过200字', 'error');
      return false;
    }
    // 获取联系方式
    params['phone'] = $('input[name="phone"]').val();
    if (params['phone'].length <= 0) {
      topAlert('请输入正确的联系电话', 'error');
      return false;
    }
    // 获取场地密码
    params['password'] = $('input[name="password"]').val();
    if (params['password'].length != 6) {
      topAlert('请输入有效的6位场地密码', 'error');
      return false;
    }
    // 获取价格
    params['price'] = $('input[name="price"]').val();
    // 获取容量
    params['capacity'] = $('input[name="capacity"]').val();
    // 获取注意事项
    params['notice'] = dumpsNewline($('textarea[name="notice"]').val());
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
    topAlert('正在创建商店,请勿关闭页面');
    post('/admin/shop?action=add', params, function(msg) {
      topAlert('创建场地成功');
    });
  })
}

var getBookableTime = function(params) {
  params['invalide_times'] = [];
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
    params['invalide_times'].push({'startTime' : startTime.Format('yyyy-MM-dd hh:mm:ss'), 'endTime' : endTime.Format('yyyy-MM-dd hh:mm:ss')});
  });
  if (!error)
    return error
  params['invalide_times'] = JSON.stringify(params['invalide_times']);
  return params
}

var getCoverMedia = function(params) {
  // 获取封面类型
  params['cover_type'] = $('.radio.checked').attr('value');
  // 获取封面内容
  params['cover'] = []
  if (params['cover_type'] == 'image') {
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