var bindNumberInputCallback = function(callback) {
  $('.numberInputBtn').on('tap', function() {
    var value = $(this).attr('value');
    callback(value);
  });
}