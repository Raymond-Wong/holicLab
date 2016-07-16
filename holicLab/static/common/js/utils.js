var post = function(url, data, callback) {
  alert(url);
  alert(data);
  $.post(url, data, function(res) {
    if (res['code'] == '0') {
      callback(res['msg']);
    } else {
      alert(res['msg']);
    }
  });
}

var tzAware = function(date) {
  date.setHours(date.getHours() - date.getTimezoneOffset() / 60);
  return date
}

// 月(M)、日(d)、小时(h)、分(m)、秒(s)、季度(q) 可以用 1-2 个占位符，   
// 年(y)可以用 1-4 个占位符，毫秒(S)只能用 1 个占位符(是 1-3 位的数字)   
// 例子：   
// (new Date()).Format("yyyy-MM-dd hh:mm:ss.S") ==> 2006-07-02 08:09:04.423   
// (new Date()).Format("yyyy-M-d h:m:s.S")      ==> 2006-7-2 8:9:4.18
Date.prototype.Format = function(fmt) { //author: meizz   
  var o = {   
    "M+" : this.getMonth()+1,                 //月份   
    "d+" : this.getDate(),                    //日   
    "h+" : this.getHours(),                   //小时   
    "m+" : this.getMinutes(),                 //分   
    "s+" : this.getSeconds(),                 //秒   
    "q+" : Math.floor((this.getMonth()+3)/3), //季度   
    "S"  : this.getMilliseconds()             //毫秒   
  };   
  if(/(y+)/.test(fmt))   
    fmt=fmt.replace(RegExp.$1, (this.getFullYear()+"").substr(4 - RegExp.$1.length));   
  for(var k in o)   
    if(new RegExp("("+ k +")").test(fmt))   
  fmt = fmt.replace(RegExp.$1, (RegExp.$1.length==1) ? (o[k]) : (("00"+ o[k]).substr((""+ o[k]).length)));   
  return fmt;
}

function getUrlParam(name) {
  var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)"); //构造一个含有目标参数的正则表达式对象
  var r = window.location.search.substr(1).match(reg);  //匹配目标参数
  if (r != null) return unescape(r[2]); return null; //返回参数值
}

var wxConfig = function(jsApiList) {
  var appId = 'wx466a0c7c6871bc8e';
  var url = window.location.href.split('#')[0];
  alert('wxConfig starting');
  post('/wechat/config', {'url' : url}, function(msg) {
    var signature = msg['signature'];
    var timestamp = msg['timestamp'];
    var nonceStr = msg['noncestr'];
    alert(msg.join('; ') + ' 开始初始化jsapi');
    wx.config({
      debug: true, // 开启调试模式,调用的所有api的返回值会在客户端alert出来，若要查看传入的参数，可以在pc端打开，参数信息会通过log打出，仅在pc端时才会打印。
      appId: appId, // 必填，公众号的唯一标识
      timestamp: timestamp, // 必填，生成签名的时间戳
      nonceStr: nonceStr, // 必填，生成签名的随机串
      signature: signature,// 必填，签名，见附录1
      jsApiList: jsApiList // 必填，需要使用的JS接口列表，所有JS接口列表见附录2
    });
  });
  wx.error(function(res){
    alert(res);
  });
}

var getAddressLocation = function(address, callback) {
  var geocoder = new qq.maps.Geocoder();
  //对指定地址进行解析
  geocoder.getLocation(address);
  //设置服务请求成功的回调函数
  geocoder.setComplete(function(result) {
    callback(result.detail)
  });
  //若服务请求失败，则运行以下函数
  geocoder.setError(function() {
    alert("无法在地图上找到以下位置：" + address);
  });
}