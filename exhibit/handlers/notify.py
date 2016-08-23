# -*- coding: utf-8 -*-
import sys
sys.path.append('..')
reload(sys)
sys.setdefaultencoding('utf-8')
import json
from datetime import timedelta
try: 
  import xml.etree.cElementTree as ET
except ImportError: 
  import xml.etree.ElementTree as ET

from django.http import HttpResponse, HttpRequest, HttpResponseServerError, Http404
from django.utils.encoding import smart_str
from django.db.models import F

from holicLab.utils import *
import holicLab.settings as settings
from holicLab.models import Order, Shop, User, Course, Bookable_Time, Time_Bucket
from pay import getOrderPrice, successOrder

def notify(request):
  # 待返回信息
  RET_STR = '<xml><return_code><![CDATA[%s]]></return_code><return_msg><![CDATA[%s]]></return_msg></xml>'
  # 获取请求参数
  params = ET.fromstring(smart_str(request.body))
  params = xml2dict(params)
  if params['return_code'] != 'SUCCESS':
    return HttpResponse(RET_STR % ('FAIL', 'communication error'))
  order = Order.objects.get(oid=params['out_trade_no'])
  # 验证签名
  if not verifySign(params, order):
    return RET_STR % ('FAIL', 'sign verification failed')
  # 如果订单已经被处理过，则直接返回修改成功
  if order.state != "1":
    return RET_STR % ('SUCCESS', 'order has been processed')
  if params['return_code'] == 'SUCCESS':
    successOrder(order, params['result_code'], params['time_end'])
  return HttpResponse(RET_STR % ('SUCCESS', 'OK'))

# 验证签名是否正确
def verifySign(params, order):
  givenSign = params.pop('sign')
  toSignStr = '&'.join(map(lambda x:x[0] + '=' + x[1], sorted(params.iteritems(), lambda x,y:cmp(x[0], y[0]))))
  toSignStr += ('&key=' + settings.WX_MCH_KEY)
  sign = md5(toSignStr).upper()
  return givenSign == sign