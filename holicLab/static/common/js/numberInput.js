var bindNumberInputCallback = function(callback) {
  $('.numberInputText').on('tap', function() {
    $('body').prepend('tap ');
    var value = $(this).parent().attr('value');
    callback(value);
  });
}