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
      print order.duration
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
    now = timezone.now()
    now += timedelta(minutes=15)
    order = user.order_set.filter(start_time__lte=now).filter(end_time__gt=now)
    if len(order) == 0:
      return HttpResponse(Response(c=1, m='获取密码失败，请在预约时间前15分钟点击获取密码').toJson(), content_type="application/json")
    order = order[0]
    return HttpResponse(Response(m='/order?action=password&oid=%s' % str(order.oid)).toJson(), content_type="application/json")
  url = 'http://holicLab.applinzi.com/order?action=get&oid=' + request.GET.get('oid')
  img = qrcode.make(url)
  img_buffer = cStringIO.StringIO()
  img.save(img_buffer, format='PNG')
  qrcode = 'data:image/png;base64,' + base64.b64encode(img_buffer.getvalue())
  return render(request, 'exhibit/order_password.html', {'order' : order, 'qrcode' : qrcode})



