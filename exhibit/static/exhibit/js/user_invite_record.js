var balance = 0;
var uid = null;

$(document).ready(function() {
  getMetaInfo();
  alert(balance);
  alert(uid);
});

var getMetaInfo = function() {
  var line = $('.infoLine');
  balance = parseInt(line.attr('balance'));
  uid = line.attr('uid');
  line.remove();
}