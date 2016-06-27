$(document).ready(function() {
  deleteShop();
  releaseShop();
  calendarAction();
});

var calendarAction = function() {
  $('.calendarBtn').click(function() {
    window.location.href = $(this).parent().parent().attr('href') + '#bookStepBox';
    return false;
  });
}

var deleteShop = function() {
  $('.shopBox .deleteBtn').click(function() {
    var sid = $(this).parent().parent().attr('sid');
    var name = $(this).parent().children('.shopName').text();
    if (!confirm("确定删除场地\"" + name + "\"吗？\n删除的场地将无法恢复"))
      return false;
    post('/admin/shop?action=delete', {'sid' : sid}, function(msg) {
      window.location.href = '/admin/shop?action=list';
    });
    return false;
  });
}

var releaseShop = function() {
  $('.releaseBtn').click(function() {
    var shopBox = $(this).parent().parent();
    var sid = shopBox.attr('sid');
    var name = $(this).parent().children('.shopName').text();
    if (!confirm('确定发布场地"' + name + '"吗？\n已发布的场地将无法下架'))
      return false;
    post('/admin/shop?action=release', {'sid' : sid}, function(msg) {
      window.location.href = '/admin/shop?action=list';
    });
    return false;
  });
}