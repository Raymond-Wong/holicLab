var post = function(url, data, callback) {
  $.post(url, data, function(res) {
    console.log(res);
    if (res['code'] == '0') {
      callback(res['msg']);
    } else {
      topAlert(res['msg'], 'error');
    }
  });
}