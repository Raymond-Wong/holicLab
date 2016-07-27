var bindNumberInputCallback = function(callback) {
  $('.numberInputBtn').on('tap', function() {
    $('body').prepend('tap ');
    var value = $(this).attr('value');
    callback(value);
  });
}