$(document).ready(function() {
  wxConfig(['onMenuShareAppMessage']);
  wx.ready(function() {
    alert(wx);
  });
  myScroll = new IScroll('#courseWrapper', { scrollX: true, scrollY: false, mouseWheel: true, eventPassthrough: true});
})