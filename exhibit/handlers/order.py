# -*- coding: utf-8 -*-
import sys
sys.path.append('..')
reload(sys)
sys.setdefaultencoding('utf-8')
import json
from datetime import timedelta

from django.http import HttpResponse, HttpRequest, HttpResponseServerError, Http404
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers

from holicLab.utils import *
from holicLab.models import Order, Shop, User

def add(request):
  pass

def pre(request):
  order_type = request.GET.get('type', None)
  if order_type == 'site':
    return pre_site_order(request)
  elif order_type == 'course':
    return pre_course_order(request)
  return HttpResponse(Response(c=1, m="待添加订单类型错误").toJson(), content_type="application/json")

def pre_site_order(request):
  # 判断数据合法性
  sid = request.GET.get('sid', None)
  shop = None
  timestamp = request.GET.get('timestamp', None)
  print timestamp
  try:
    shop = Shop.objects.get(id=int(sid))
  except Exception:
    return HttpResponse(Response(c=2, m='待预定场地不存在').toJson(), content_type='application/json')
  start_time = datetime.fromtimestamp(float(timestamp))
  now = datetime.now()
  if start_time < now:
    print start_time, now
    return HttpResponse(Response(c=3, m='待预约时间已过期').toJson(), content_type='application/json')
  params = {}
  user = User.objects.get(invite_code=request.session['user'])
  params['is_first_order'] = True if len(user.order_set.filter(order_type=4)) == 0 else False
  params['balance'] = user.balance
  params['cover'] = json.loads(shop.cover)[0]
  params['title'] = shop.name
  params['startTime'] = start_time.strftime('%a, %b %d, %H:%M')
  params['location'] = shop.location
  params['price'] = shop.price
  params['capacity'] = shop.capacity
  params['bookable_time'] = []
  current_time = start_time
  for i in xrange(1, 4):
    current_time = current_time + timedelta(minutes=i * 30)
    params['bookable_time'].append({'duration' : (i + 1) * 30, 'bookable' : True if getTimeOccupation(shop, current_time) < shop.capacity else False})
  params['bookable_amount'] = []
  start_time_occupation = getTimeOccupation(shop, start_time)
  for i in xrange(1, 4):
    if start_time_occupation + i < shop.capacity:
      params['bookable_amount'].append(i)
  if start_time_occupation == 0:
    params['bookable_amount'].append('包场')
  return render(request, 'exhibit/order_pre.html', params)

def getTimeOccupation(shop, time):
  time_bucket = shop.time_bucket_set.filter(start_time=time)
  ret = 0
  if len(time_bucket):
    ret = time_bucket[0].occupation
  return ret

def pre_course_order(request):
  pass

def list(request):
  invite_code = request.session['user']
  user = None
  try:
    user = User.objects.get(invite_code=invite_code)
  except:
    return HttpResponse(Response(c=-2, m="待查询用户不存在").toJson(), content_type="application/json")
  orders = user.order_set.all()
  return render(request, 'exhibit/order_list.html', {'orders' : orders})

def get(request):
  oid = request.GET.get('oid', None)
  if oid is None:
    return HttpResponse(Response(c=-9, m="未提供待查询订单id").toJson(), content_type="application/json")
  order = None
  try:
    order = Order.objects.get(id=oid)
  except:
    return HttpResponse(Response(c=-5, m="待查询订单不存在").toJson(), content_type="application/json")
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