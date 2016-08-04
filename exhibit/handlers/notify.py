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

from holicLab.utils import *
from holicLab.models import Order, Shop, User, Course, Bookable_Time

def notify(request):
  # 待返回信息
  RET_STR = '<xml><return_code><![CDATA[%s]]></return_code><return_msg><![CDATA[%s]]></return_msg></xml>'
  # 获取请求参数
  # params = ET.fromstring(smart_str(request.body))
  # params = xml2dict(params)
  # if params['return_code'] != 'SUCCESS':
  #   return HttpResponse(RET_STR % ('FAIL', 'communication error'))
  # order = Order.objects.get(oid=params['out_trade_no'])
  # # 验证签名
  # if not verifySign(params, order):
  #   return RET_STR % ('FAIL', 'sign verification failed')
  # # 如果订单已经被处理过，则直接返回修改成功
  # if order.state != "1":
  #   return RET_STR % ('SUCCESS', 'order has been processed')
  # if params['result_code'] == 'SUCCESS':
  #   # 更新订单对象
  #   updateOrderObject(params, order)
  #   # 更新订单状态为success
  #   order.state = "4"
  # else:
  #   # 更新订单状态为cancel
  #   order.state = "2"
  # order.save()
  return HttpResponse(RET_STR % ('SUCCESS', 'OK'))

# 验证签名是否正确
def verifySign(params, order):
  return True

# 付款成功后更新订单状态以及订单对象状态
def updateOrderObject(params, order):
  # 更新被预定对象的信息
  if order.order_type == "1":
    shop = order.shop
    timeBucket = Time_Bucket.objects.filter(shop=shop).get(start_time=order.start_time)
    timeBucket.occupation = F('occupation') + 1
    timeBucket.save()
  else:
    course = order.course
    bookableTime = Bookable_Time.objects.filter(course=course).get(start_time=order.start_time)
    bookableTime.occupation = F('occupation') + 1
    bookableTime.save()