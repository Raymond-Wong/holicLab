var bindNumberInputCallback = function(callback) {
  $('.numberInputBtn').click(function() {
    var value = $(this).attr('value');
    callback(value);
  });
}