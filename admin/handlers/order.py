# -*- coding: utf-8 -*-
import sys
sys.path.append('..')
reload(sys)
sys.setdefaultencoding('utf-8')
import json
import time
import datetime

from django.http import HttpResponse, HttpRequest, HttpResponseServerError, Http404
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers

from holicLab.utils import *
from holicLab.models import Order, Shop

def deleteOrders(orders):
  for order in orders:
    order.delete()

def list(request):
  if request.method == 'GET':
    state = request.GET.get('state', 'unfinished')
    if state == 'finished':
      orders = Order.objects.filter(state__in=[2,3,4])
    elif state == 'unfinished':
      orders = Order.objects.filter(state=1)
    else:
      orders = Order.objects.all()
    return render(request, 'admin/order.html', {'orders' : orders, 'activePage' : 'order'})
  orders = Order.objects.all()
  # 商店
  sid = request.POST.get('sid', None)
  shop = None
  if sid is not None:
    try:
      shop = Shop.objects.get(id=int(sid))
    except:
      return HttpResponse(Response(c=-3, m='待查询商店不存在').toJson(), content_type='application/json')
    orders.filter(shop=shop)
  # 用户
  uid = request.POST.get('uid', None)
  user = None
  if uid is not None:
    try:
      user = User.objects.get(id=int(uid))
    except:
      return HttpResponse(Response(c=-2, m='待查询用户不存在').toJson(), content_type='application/json')
    orders.filter(user=user)
  # 课程
  cid = request.POST.get('cid', None)
  course = None
  if cid is not None:
    try:
      course = Course.objects.get(id=int(cid))
    except:
      return HttpResponse(Response(c=-4, m='待查询课程不存在').toJson(), content_type='application/json')
    orders.filter(course=course)
  # 练习开始时间
  start_time = request.POST.get('start_time', None)
  if start_time is not None:
    try:
      start_time = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
    except:
      return HttpResponse(Response(c=-10, m='时间格式错误').toJson(), content_type='application/json')
    orders.filter(end_time__gte=start_time)
  # 练习结束时间
  end_time = request.POST.get('end_time', None)
  if end_time is not None:
    try:
      end_time = datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
    except:
      return HttpResponse(Response(c=-10, m='时间格式错误').toJson(), content_type='application/json')
    orders.filter(start_time__lt=end_time)
  # 订单创建时间
  create_time_lb = request.POST.get('create_time_lb', '2000-1-1 0:0:0')
  create_time_ub = request.POST.get('create_time_ub', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
  try:
    create_time_lb = datetime.datetime.strptime(create_time_lb, '%Y-%m-%d %H:%M:%S')
    create_time_ub = datetime.datetime.strptime(create_time_ub, '%Y-%m-%d %H:%M:%S')
  except:
    return HttpResponse(Response(c=-10, m='时间格式错误').toJson(), content_type='application/json')
  orders.filter(create_time__gte=create_time_lb).filter(create_time__lt=create_time_ub)
  return HttpResponse(Response(m=serializers.serialize("json", orders)).toJson(), content_type='application/json')
