var isFirstOrder = false;
var balance = 0;
var price = null;
var capacity = null;

$(document).ready(function() {
  getMetaInfo();
  updatePrice();
  updatePriceAction();
  checkBoxAction();
});

var updatePriceAction = function() {
  $('.radio, .checkBox').on('touchstart', function() {
    updatePrice();
  });
}

var getMetaInfo = function() {
  var line = $('.infoLine');
  isFirstOrder = line.attr('isFirstOrder') == 'True' ? true : false;
  balance = parseInt(line.attr('balance') == '' ? '0' : line.attr('balance'));
  price = parseInt(line.attr('price'));
  capacity = parseInt(line.attr('capacity'));
  line.remove();
}

var checkBoxAction = function() {
  $('.serviceLine').click(function() {
    var checkbox = $(this).children('.checkBox');
    checkbox.trigger('click');
  })
}

var updatePrice = function() {
  var totalPrice = price;
  // 增值服务
  $('.serviceLine').each(function() {
    var checkbox = $(this).children('.checkBox');
    var price = parseInt($(this).attr('price'));
    if (checkbox.hasClass('checked'))
      totalPrice += price;
  });
  // 时长
  if (getUrlParam['type'] == 'site') {
    var duration = parseInt($('.radio.checked[name="duration"]').attr('value')) / 30;
    totalPrice += duration * price;
  }
  // 人数
  var amount = parseInt($('.radio.checked[name="amount"]').attr('value'));
  totalPrice *= amount
  var discountPrice = totalPrice;
  // 首单五折
  if (isFirstOrder) {
    discountPrice /= 2;
  } else if (duration != undefined) {
    // 如果不是首单则每小时可以使用一张优惠券
    coupon = parseInt(duration / 2);
    coupon = coupon > balance ? balance : coupon;
    discountPrice -= (coupon * 100);
  }
  // 更新价格
  $('.discountPrice').text('￥' + (parseFloat(discountPrice) / 10));
  $('.originPrice').text('￥' + (parseFloat(totalPrice) / 10));
}