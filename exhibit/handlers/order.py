# -*- coding: utf-8 -*-
import sys
sys.path.append('..')
reload(sys)
sys.setdefaultencoding('utf-8')
import json
import time
from datetime import timedelta

from django.http import HttpResponse, HttpRequest, HttpResponseServerError, Http404
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.utils import timezone

from holicLab.utils import *
from holicLab.models import Order, Shop, User, Course, Bookable_Time

def add(request):
  user = User.objects.get(invite_code=request.session['user'])
  newOrder = Order()
  newOrder.order_type = int(request.POST.get('type', None))
  newOrder.user = user
  newOrder.oid = md5(user.invite_code + str(time.time() * 1000))
  newOrder.start_time = datetime.strptime(request.POST.get('start_time', None), '%a, %d %b %Y, %H:%M')
  newOrder.end_time = newOrder.start_time + timedelta(minutes=int(request.POST.get('duration', None)))
  newOrder.people_amout = int(request.POST.get('amount', None))
  print request.POST.get('services', None)
  newOrder.services = request.POST.get('services', [])
  # 计算基础价格
  newOrder.price = 0
  if newOrder.order_type == 1:
    newOrder.shop = Shop.objects.get(id=request.POST.get('sid'))
    newOrder.price = newOrder.shop.price
  else:
    newOrder.course = Course.objects.get(id=request.POST.get('cid'))
    newOrder.shop = newOrder.course.shop
    newOrder.price = newOrder.course.price
  newOrder.price = int(request.POST.get('duration', None)) / 30 * newOrder.price
  for service in newOrder.services:
    if service == 'food':
      newOrder.price += 500
    elif service == 'coach':
      newOrder.price += 1000
  newOrder.price = newOrder.people_amount * price
  # 计算优惠
  if len(user.order_set.all()) == 0:
    newOrder.price = newOrder.price / 2
  else:
    coupon = request.POST.get('duration', None) / 60
    coupon = coupon if user.balance > coupon else user.balance
    newOrder.price = newOrder.price - 100 * coupon
  newOrder.save()
  return HttpResponse(Response(m="添加订单成功").toJson(), content_type="application/json")

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
  try:
    shop = Shop.objects.get(id=int(sid))
  except Exception:
    return HttpResponse(Response(c=2, m='待预定场地不存在').toJson(), content_type='application/json')
  start_time = datetime.fromtimestamp(float(timestamp))
  now = datetime.now()
  if start_time < now:
    return HttpResponse(Response(c=3, m='待预约时间已过期').toJson(), content_type='application/json')
  params = {}
  user = User.objects.get(invite_code=request.session['user'])
  params['is_first_order'] = True if len(user.order_set.filter(order_type=4)) == 0 else False
  params['balance'] = user.balance
  params['cover'] = json.loads(shop.cover)[0]
  params['title'] = shop.name
  params['startTime'] = start_time.strftime('%a, %d %b %Y, %H:%M')
  params['location'] = shop.location
  params['type'] = 'site'
  params['price'] = shop.price
  params['capacity'] = shop.capacity
  params['id'] = shop.id
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
    # 判断数据合法性
  cid = request.GET.get('cid', None)
  bid = request.GET.get('bid', None)
  course = None
  to_book_time = None
  try:
    course = Course.objects.get(id=int(cid))
  except Exception:
    return HttpResponse(Response(c=2, m='待预定课程不存在').toJson(), content_type='application/json')
  try:
    to_book_time = Bookable_Time.objects.get(id=int(bid))
  except Exception, e:
    return HttpResponse(Response(c=3, m='待预定课程在待预定时间内没开课').toJson(), content_type='application/json')
  now = timezone.now()
  if to_book_time.start_time < now:
    return HttpResponse(Response(c=4, m='待预约时间已过期').toJson(), content_type='application/json')
  params = {}
  user = User.objects.get(invite_code=request.session['user'])
  params['is_first_order'] = True if len(user.order_set.filter(order_type=4)) == 0 else False
  params['balance'] = user.balance
  params['cover'] = json.loads(course.cover)[0]
  params['title'] = course.name
  params['type'] = 'course'
  params['startTime'] = timezone.localtime(to_book_time.start_time).strftime('%a, %b %d, %H:%M') + '-' + timezone.localtime(to_book_time.end_time).strftime('%H:%M')
  params['location'] = course.shop.location
  params['price'] = course.price
  params['capacity'] = course.capacity
  params['id'] = course.id
  params['bookable_amount'] = []
  for i in xrange(1, 4):
    if to_book_time.occupation + i < course.capacity:
      params['bookable_amount'].append(i);
  if to_book_time.occupation == 0:
    params['bookable_amount'].append('包场')
  return render(request, 'exhibit/order_pre.html', params)

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