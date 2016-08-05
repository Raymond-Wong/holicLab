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
from holicLab.models import Order, Shop, User, Course, Bookable_Time

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
  return True

# 订单支付成功后修改数据
def successOrder(order, status, time_end):
  # 1. 修改订单的状态
  if status == 'SUCCESS':
    order.state = "4"
    order.pay_time = datetime.strptime(time_end, '%Y%m%d%H%M%S')
  else:
    order.state = "2"
    return order.save()
  # 2. 设置该用户为老用户
  user = order.user
  user.user_type = "2"
  # 3. 如果该用户第一次下单且是被邀请用户的话，邀请他的用户可以获得优惠券
  if user.invited_by and len(user.order_set.filter(state="4")) == 1:
    invite_user = User.objects.get(invite_code=user.invited_by)
    invite_user.balance = F('balance') + 1
    invite_user.save()
  # 4. 修改订单涉及课程或者场地的占用人次
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
  # 保存对象
  order.save()
  user.save()