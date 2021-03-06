$(document).ready(function() {
  deleteCourse();
  releaseCourse();
  calendarAction();
});

var calendarAction = function() {
  $('.calendarBtn').click(function() {
    window.location.href = '/admin/course?action=calendar&cid=' + $(this).attr('cid');
    // window.location.href = $(this).parent().parent().attr('href') + '#bookStepBox';
    return false;
  });
}

var deleteCourse = function() {
  $('.shopBox .deleteBtn').click(function() {
    var sid = $(this).parent().parent().attr('cid');
    var name = $(this).parent().children('.shopName').text();
    if (!confirm("确定删除课程\"" + name + "\"吗？\n删除的课程将无法恢复"))
      return false;
    post('/admin/course?action=delete', {'cid' : sid}, function(msg) {
      window.location.href = '/admin/course?action=list&sid=' + $('.shopWrapper').attr('sid');
    });
    return false;
  });
}

var releaseCourse = function() {
  $('.releaseBtn').click(function() {
    var shopBox = $(this).parent().parent();
    var cid = shopBox.attr('cid');
    var sid = $('.shopWrapper').attr('sid');
    var name = $(this).parent().children('.shopName').text();
    if (!confirm('确定发布场地"' + name + '"吗？\n已发布的课程将无法下架'))
      return false;
    post('/admin/course?action=release', {'cid' : cid}, function(msg) {
      window.location.href = '/admin/course?action=list&sid=' + sid;
    });
    return false;
  });
}