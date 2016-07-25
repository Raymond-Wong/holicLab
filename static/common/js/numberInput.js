var bindNumberInputCallback = function(callback) {
  $('.numberInputBtn').on('touchend', function() {
    var value = $(this).attr('value');
    callback(value);
  });
}