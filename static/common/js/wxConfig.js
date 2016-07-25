var wxConfig = function(jsApiList) {
  var appId = 'wx466a0c7c6871bc8e';
  var url = window.location.href.split('#')[0];
  post('/wechat/config', {'url' : url}, function(msg) {
    var signature = msg['signature'];
    var timestamp = msg['timestamp'];
    var nonceStr = msg['noncestr'];
    wx.config({
      debug: true, // 开启调试模式,调用的所有api的返回值会在客户端alert出来，若要查看传入的参数，可以在pc端打开，参数信息会通过log打出，仅在pc端时才会打印。
      appId: appId, // 必填，公众号的唯一标识
      timestamp: timestamp, // 必填，生成签名的时间戳
      nonceStr: nonceStr, // 必填，生成签名的随机串
      signature: signature,// 必填，签名，见附录1
      jsApiList: jsApiList // 必填，需要使用的JS接口列表，所有JS接口列表见附录2
    });
  });
  wx.error(function(res){
    alert(res);
  });
}

$(document).ready(function() {
  wxConfig(['onMenuShareAppMessage']);
  wx.ready(function() {
      wx.onMenuShareAppMessage({
        title: 'Holic Lab 健身试炼仓', // 分享标题
        desc: '你的好友邀请你一起来健身', // 分享描述
        link: window.location.href, // 分享链接
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
  });
});
