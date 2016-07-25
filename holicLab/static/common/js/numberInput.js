var bindNumberInputCallback = function(callback) {
  $('.numberInputBtn').on('click', function() {
    var value = $(this).attr('value');
    callback(value);
  });
}