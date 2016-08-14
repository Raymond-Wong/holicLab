$(document).ready(function() {
  $('#submitBtn').click(function() {
  	var url="/admin/login";
  	var account = $('input[name="account"]').val();
  	if (account == '') {
  	  topAlert("账号不能为空", 'error')
  	  return;
  	}
  	var password = $('input[name="password"]').val();
  	if (password == '') {
  	  topAlert("密码不能为空", 'error')
  	  return;
  	}
  	var params = {'account' : $.md5(account), 'password' : $.md5(password)};
    post(url, params, function(msg) {
      window.location.href=msg;
    })
  });
  // 监听回车
  listenReturn();
});

var listenReturn = function() {
  $(window).keydown(function(e) {
    if (e.keyCode == 13) {
      $('#submitBtn').trigger('click');
    }
  });
}