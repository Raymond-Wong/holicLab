var bindNumberInputCallback = function(callback) {
  $('.numberInputBtn').on('tap', function() {
    var mask = $(this).children('.numberInputMask');
    mask.stop();
    mask.css('opacity', '0.5');
    var value = $(this).attr('value');
    callback(value);
    mask.animate({opacity : '0'}, 700);
    return false;
  });
}