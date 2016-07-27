var bindNumberInputCallback = function(callback) {
  $('.numberInputBtn').on('tap', function() {
    $('body').prepend('tap1 ');
    var value = $(this).attr('value');
    callback(value);
    return false;
  });
}