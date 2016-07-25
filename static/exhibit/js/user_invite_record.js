var balance = 0;
var uid = null;

$(document).ready(function() {
  getMetaInfo();
  initRecord();
  initShare();
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

var initShare = function() {
  wxConfig(['onMenuShareAppMessage']);
  wx.ready(function() {
    wx.onMenuShareAppMessage({
      title: 'Holic Lab 健身试炼仓', // 分享标题
      desc: '你的好友邀请你一起来健身', // 分享描述
      link: window.location.host + '/user?action=invite&invited=' + uid, // 分享链接
      imgUrl: '', // 分享图标
      type: 'link', // 分享类型,music、video或link，不填默认为link
      dataUrl: '', // 如果type是music或video，则要提供数据链接，默认为空
      success: function () { 
        // 用户确认分享后执行的回调函数
      },
      cancel: function () { 
        // 用户取消分享后执行的回调函数
      }
    });
  })
}