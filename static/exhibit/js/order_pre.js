var isFirstOrder = false;
var balance = 0;
var price = null;
var capacity = null;
var orderType = 'site';
var targetId = null;

$(document).ready(function() {
  wxInit();
  getMetaInfo();
  updatePrice();
  updatePriceAction();
  checkBoxAction();
  submitAction();
});

var wxInit = function() {
  wxConfig(['chooseWXPay']);
}

var submitAction = function() {
  $('#payBtn').on('tap', function() {
    $(this).attr('disabled', true);
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
    post('/order/pay?action=add', params, function(msg) {
      wx.ready(function() {
        wx.chooseWXPay({
          timestamp: msg['timeStamp'], // 支付签名时间戳，注意微信jssdk中的所有使用timestamp字段均为小写。但最新版的支付后台生成签名使用的timeStamp字段名需大写其中的S字符
          nonceStr: msg['nonceStr'], // 支付签名随机串，不长于 32 位
          package: msg['package'], // 统一支付接口返回的prepay_id参数值，提交格式如：prepay_id=***）
          signType: msg['signType'], // 签名方式，默认为'SHA1'，使用新版支付需传入'MD5'
          paySign: msg['paySign'], // 支付签名
          success: function (res) {
            alert('支付成功！');
          },
          cancel: function(res) {
            alert('付款遇到问题了吗？请联系我们的客户哦～')
          }
        });
      });
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
  post('/order/pay?action=price', params, function(msg) {
    $('.discountPrice').text('￥' + (parseFloat(msg) / 10));
  });
}