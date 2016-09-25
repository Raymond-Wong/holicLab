$(document).ready(function() {
  $('.submitBtn').click(function() {
    var url = $('#inputHref').val();
    $('#outputHref').val('转换中...');
    setTimeout(function() {
      post('/admin/url', {'url' : url}, function(msg) {
        $('#outputHref').val(msg);
      });
    }, 500);
  });
});