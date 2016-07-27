var bindNumberInputCallback = function(callback) {
  $('.numberInputBtn').on('tap', function() {
    alert('tap number input');
    var value = $(this).attr('value');
    callback(value);
  });
}