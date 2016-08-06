$(document).ready(function() {
  wxConfig(['hideOptionMenu']);
  wx.ready(function() {
    wx.hideOptionMenu();
  });
});