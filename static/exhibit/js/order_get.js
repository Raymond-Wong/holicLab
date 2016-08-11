var uid = null;

$(document).ready(function() {
  getMetaInfo();
  initShare();
  initInviteAction();
  initCancelAction();
});

var initCancelAction = function() {
  $('#cancelBtn').on('tap', function() {
    var oid = $(this).attr('oid');
    post('/order?action=cancel', {'oid' : oid}, function(msg) {
      alert(msg);
    });
  });
}

var getMetaInfo = function() {
  uid = $('#shareMask').attr('uid');
  $('#shareMask').removeAttr('uid');
}

var initInviteAction = function() {
  $('.shareBtn').on('tap', function() {
    $('#shareMask').show();
    $('#shareMask').bind('tap', function() {
      $(this).hide();
      $(this).unbind('tap');
    });
    return false;
  });
}

var initShare = function() {
  wxConfig(['onMenuShareAppMessage', 'showMenuItems']);
  wx.ready(function() {
    wx.showMenuItems({
      menuList: ['menuItem:share:appMessage'] // 要显示的菜单项，所有menu项见附录3
    });
    var link = 'http://' + window.location.host + '/user?action=invite&invited=' + uid;
    link = encodeURIComponent(link);
    link = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx8a6f32cf9d22a289&redirect_uri=' + link + '&response_type=code&scope=snsapi_userinfo&state=STATE#wechat_redirect';
    wx.onMenuShareAppMessage({
      title: '来一次HolicLab吧，优惠拿去别客气！', // 分享标题
      desc: '首次预约立享五折，无需年卡，永不打烊，24小时不停摆只等你来练🏋', // 分享描述
      link: link, // 分享链接
      imgUrl: 'http://' + window.location.host + '/static/exhibit/res/user_invited.jpg', // 分享图标
      type: 'link', // 分享类型,music、video或link，不填默认为link
      dataUrl: '', // 如果type是music或video，则要提供数据链接，默认为空
      success: function () { 
        alert('分享成功！\n当被邀请用户首次下单以后，您将获得十元抵扣券一张！')
      },
      cancel: function () { 
        // 用户取消分享后执行的回调函数
      }
    });
  })
}