var isFirstOrder = false;
var balance = 0;
var price = null;
var capacity = null;
var orderType = 'site';
var targetId = null;

$(document).ready(function() {
  getMetaInfo();
  updatePrice();
  updatePriceAction();
  checkBoxAction();
  submitAction();
});

var submitAction = function() {
  $('#payBtn').on('tap', function() {
    var params = {};
    params['type'] = orderType == 'site' ? 1 : 2;
    if (params['type'] == 1) {
      params['start_time'] = $('#startTimeBox').text();
      params['duration'] = parseInt($('.radio.checked[name="duration"]').attr('value'));
    } else {
      params['bid'] = $('#startTimeBox').attr('bid');
    }
    params['amount'] = parseInt($('.radio.checked[name="amount"]').attr('value'));
    params['services'] = [];
    var services = $('.serviceLine');
    for (var i = 0; i < services.length; i++) {
      var service = $(services[i]);
      var checkbox = service.children('.checkBox');
      if (checkbox.hasClass('checked')) {
        params['services'].push(service.attr('value'));
      }
    }
    params['services'] = JSON.stringify(params['services']);
    if (orderType == 'site') {
      params['sid'] = targetId;
    } else {
      params['cid'] = targetId;
    }
    post('/order?action=add', params, function(msg) {
      alert(msg);
    });
  });
}

var updatePriceAction = function() {
  $('.checkBox, .radio').on('tap', function() {
    updatePrice();
  });
}

var getMetaInfo = function() {
  var line = $('.infoLine');
  isFirstOrder = line.attr('isFirstOrder') == 'True' ? true : false;
  balance = parseInt(line.attr('balance') == '' ? '0' : line.attr('balance'));
  price = parseInt(line.attr('price'));
  capacity = parseInt(line.attr('capacity'));
  orderType = line.attr('type');
  targetId = parseInt(line.attr('id'));
  line.remove();
}

var checkBoxAction = function() {
  $('.serviceLine').on('click', function() {
    var checkbox = $(this).children('.checkBox');
    checkbox.trigger('tap');
  })
}

var updatePrice = function() {
  $('.discountPrice').text('正在计算价格...');
  var params = {};
  params['type'] = orderType == 'site' ? 1 : 2;
  if (params['type'] == 1) {
    params['start_time'] = $('#startTimeBox').text();
    params['duration'] = parseInt($('.radio.checked[name="duration"]').attr('value'));
  } else {
    params['bid'] = $('#startTimeBox').attr('bid');
  }
  params['amount'] = parseInt($('.radio.checked[name="amount"]').attr('value'));
  params['services'] = [];
  var services = $('.serviceLine');
  for (var i = 0; i < services.length; i++) {
    var service = $(services[i]);
    var checkbox = service.children('.checkBox');
    if (checkbox.hasClass('checked')) {
      params['services'].push(service.attr('value'));
    }
  }
  params['services'] = JSON.stringify(params['services']);
  if (orderType == 'site') {
    params['sid'] = targetId;
  } else {
    params['cid'] = targetId;
  }
  post('/order?action=price', params, function(msg) {
    $('.discountPrice').text('￥' + (parseFloat(msg) / 10));
  });
}

// var updatePrice = function() {
//   var totalPrice = price;
//   // 时长
//   if (orderType == 'site') {
//     var duration = parseInt($('.radio.checked[name="duration"]').attr('value')) / 30;
//     totalPrice *= duration;
//   }
//   // 增值服务
//   $('.serviceLine').each(function() {
//     var checkbox = $(this).children('.checkBox');
//     var price = parseInt($(this).attr('price'));
//     if (checkbox.hasClass('checked'))
//       totalPrice += price;
//   });
//   // 人数
//   var amount = parseInt($('.radio.checked[name="amount"]').attr('value'));
//   totalPrice *= amount
//   var discountPrice = totalPrice;
//   // 首单五折
//   if (isFirstOrder) {
//     discountPrice /= 2;
//   } else if (duration != undefined) {
//     // 如果不是首单则每小时可以使用一张优惠券
//     coupon = parseInt(duration / 2);
//     coupon = coupon > balance ? balance : coupon;
//     discountPrice -= (coupon * 100);
//   }
//   // 更新价格
//   $('.discountPrice').text('￥' + (parseFloat(discountPrice) / 10));
//   $('.originPrice').text('￥' + (parseFloat(totalPrice) / 10));
// }