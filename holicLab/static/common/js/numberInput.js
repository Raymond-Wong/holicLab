var bindNumberInputCallback = function(callback) {
  $('.numberInputBtn').on('touchstart', function() {
    var value = $(this).attr('value');
    callback(value);
  });
}