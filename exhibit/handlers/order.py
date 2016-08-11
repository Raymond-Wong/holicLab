# -*- coding: utf-8 -*-
import sys
sys.path.append('..')
reload(sys)
sys.setdefaultencoding('utf-8')
import json
import time
import qrcode
import base64
import cStringIO
from urllib import quote
from datetime import timedelta
try: 
  import xml.etree.cElementTree as ET
except ImportError: 
  import xml.etree.ElementTree as ET

from django.http import HttpResponse, HttpRequest, HttpResponseServerError, Http404
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.utils import timezone
from django.utils.encoding import smart_str

import holicLab.settings as settings
from holicLab.utils import *
from holicLab.models import Order, Shop, User, Course, Bookable_Time

def list(request):
  invite_code = request.session['user']
  orderType = request.GET.get('type', '0')
  user = None
  try:
    user = User.objects.get(invite_code=invite_code)
  except:
    return HttpResponse(Response(c=-2, m="待查询用户不存在").toJson(), content_type="application/json")
  if orderType == "1" or orderType == "2":
    orders = user.order_set.filter(state="4").filter(order_type=orderType)
  else:
    orders = user.order_set.filter(state="4")
    orderType = "0"
  # 处理duration
  for order in orders:
    order.price = int(order.price / 10.0)
    if order.order_type == "1":
      order.duration = order.end_time - order.start_time
      order.duration = order.duration.seconds / 60.0
      order.duration = str(int(order.duration)) + 'min'
  return render(request, 'exhibit/order_list.html', {'orders' : orders, 'type' : orderType})

def get(request):
  oid = request.GET.get('oid', None)
  if oid is None:
    return HttpResponse(Response(c=-9, m="未提供待查询订单id").toJson(), content_type="application/json")
  order = None
  try:
    order = Order.objects.get(oid=oid)
  except:
    return HttpResponse(Response(c=-5, m="待查询订单不存在").toJson(), content_type="application/json")
  if order.order_type == "1":
    order.cover = json.loads(order.shop.cover)[0]
  else:
    order.cover = json.loads(order.course.cover)[0]
  order.services = json.loads(order.services)
  if 'food' in order.services:
    order.food = True
  if 'coach' in order.services:
    order.coach = True
  order.price /= 10.0
  if order.state == "2" or order.start_time <= timezone.now():
    order.cancelable = False
  else:
    order.cancelable = True
  return render(request, 'exhibit/order_get.html', {'order' : order})

def update(request):
  oid = request.GET.get('oid', None)
  if oid is None:
    return HttpResponse(Response(c=-9, m="未提供待查询订单id").toJson(), content_type="application/json")
  order = None
  try:
    order = Order.objects.get(id=oid)
  except:
    return HttpResponse(Response(c=-5, m="待查询订单不存在").toJson(), content_type="application/json")
  order.state = 4
  order.save()
  return HttpResponse(Response(m="订单状态更新成功").toJson(), content_type="application/json")

def password(request):
  if request.method == 'POST':
    user = User.objects.get(invite_code=request.session['user'])
    start = timezone.now()
    end = start + timedelta(minutes=15)
    # order = user.order_set.filter(start_time__lte=end).filter(start_time__gte=start).filter(end_time__gt=start)
    order = user.order_set.filter(start_time__lte=end).filter(end_time__gt=end)
    if len(order) == 0:
      return HttpResponse(Response(c=1, m='获取密码失败，请在预约时间前15分钟点击获取密码').toJson(), content_type="application/json")
    order = order[0]
    return HttpResponse(Response(m='/order?action=password&oid=%s' % str(order.oid)).toJson(), content_type="application/json")
  order = Order.objects.get(oid=request.GET.get('oid'))
  url = 'http://' + request.get_host() + '/order?action=get&oid=' + request.GET.get('oid')
  url = quote(url, safe='')
  url = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx8a6f32cf9d22a289&redirect_uri=' + url + '&response_type=code&scope=snsapi_userinfo&state=STATE#wechat_redirect';
  img = qrcode.make(url)
  img_buffer = cStringIO.StringIO()
  img.save(img_buffer, format='PNG')
  qrcodeImg = 'data:image/png;base64,' + base64.b64encode(img_buffer.getvalue())
  return render(request, 'exhibit/order_password.html', {'order' : order, 'qrcode' : qrcodeImg})

def refund(request):
  print '取消订单: ' + request.POST.get('oid')
  # 获取待取消订单
  order = Order.objects.get(oid=request.POST.get('oid'))
  # 判断订单可取消金额
  now = timezone.now()
  refund = 0
  hours = int((order.start_time - now).total_seconds()) / 60 / 60
  if hours > 6:
    refund = order.price
  elif hours > 4:
    refund = order.price / 2
  if refund == 0:
    cancelSuccess(order)
    return HttpResponse(Response(m="订单取消成功,四小时内订单不退款").toJson(), content_type="application/json")
  print refund
  # 构造请求字典
  params = {}
  params['appid'] = settings.WX_APP_ID
  params['mch_id'] = settings.WX_MCH_ID
  params['device_info'] = 'WEB'
  params['nonce_str'] = random_x_bit_code(20)
  params['out_trade_no'] = order.oid
  params['out_refund_no'] = order.oid
  params['total_fee'] = "1" # order.price
  params['refund_fee'] = "1" # refund
  params['op_user_id'] = settings.WX_MCH_ID
  # 生成签名以及构造xml
  toSignStr = '&'.join(map(lambda x:x[0] + '=' + x[1], sorted(params.iteritems(), lambda x,y:cmp(x[0], y[0]))))
  toSignStr += ('&key=' + settings.WX_MCH_KEY)
  xml = dict2xml(ET.Element('xml'), params)
  signNode = ET.SubElement(xml, 'sign')
  signNode.text = md5(toSignStr).upper()
  # 发送退款请求
  msg = ET.tostring(xml, 'utf-8')
  res = send_xml_ssl('https://api.mch.weixin.qq.com/secapi/pay/refund', msg)
  res = ET.fromstring(smart_str(res))
  res = xml2dict(res)
  print res
  return HttpResponse(Response(m="订单取消成功").toJson(), content_type="application/json")

def cancelSuccess(order):
  pass