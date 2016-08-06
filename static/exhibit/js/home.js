$(document).ready(function() {
  wxConfig(['hideOptionMenu']);
  wx.ready(function() {
    wx.hideOptionMenu();
  })
  myScroll = new IScroll('#courseWrapper', { scrollX: true, scrollY: false, mouseWheel: true, eventPassthrough: true});
})