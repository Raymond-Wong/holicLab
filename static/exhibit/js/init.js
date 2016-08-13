$(document).ready(function() {
  wxConfig(['hideMenuItems']);
  wx.ready(function() {
    var list = ['menuItem:share:timeline', 'menuItem:share:qq', 'menuItem:share:weiboApp', 'menuItem:favorite', 'menuItem:share:facebook', 'menuItem:share:QZone',
                'menuItem:editTag', 'menuItem:delete', 'menuItem:copyUrl', 'menuItem:originPage', 'menuItem:readMode', 'menuItem:openWithQQBrowser', 'menuItem:openWithSafari', 'menuItem:share:email', 'menuItem:share:brand'];
    alert(window.location.href);
    if (window.location.href.indexOf('/order?action=get') < 0 &&
        window.location.href.indexOf('/user?action=invite') < 0) {
      list.push('menuItem:share:appMessage');
    }
    wx.hideMenuItems({
      menuList: list,
    });
  });
});