# -*- coding: utf-8 -*-
import sys
sys.path.append('..')
reload(sys)
sys.setdefaultencoding('utf-8')
import json

from django.http import HttpResponse, HttpRequest, HttpResponseServerError, Http404
from django.shortcuts import render_to_response, redirect
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers

from holicLab.utils import *
from holicLab.models import Shop, Time_Bucket

from order import deleteOrders

# 列出所有店铺
def list(request):
  shops = Shop.objects.all()
  hasShop = True if len(shops) > 0 else False
  return render_to_response('admin/shop_list.html', {'shops' : shops, 'hasShop' : hasShop})

# 添加一个店铺
def add(request):
  if request.method == 'GET':
    return render_to_response('admin/shop_add.html')
  # 获取数据
  name = request.POST.get('name', None)
  location = request.POST.get('location', None)
  price = request.POST.get('price', None)
  capacity = request.POST.get('capacity', None)
  invalide_times = request.POST.get('invalide_times', None)
  # 判断数据有效性
  if name is None or location is None or price is None or capacity is None or invalide_times is None:
    return HttpResponse(Response(c=-9, m="未提供指定参数").toJson(), content_type='application/json')
  if len(name) > 50:
    return HttpResponse(Response(c=1, m="门店名称不得超过50字").toJson(), content_type='application/json')
  if len(location) > 200:
    return HttpResponse(Response(c=2, m="地址长度不得超过200字").toJson(), content_type='application/json')
  try:
    price = int(price)
    capacity = int(capacity)
  except:
    return HttpResponse(Response(c=3, m="单价与门店容量必须为数值").toJson(), content_type='application/json')
  if price < 0:
    return HttpResponse(Response(c=4, m="单价必须为正整数(元)").toJson(), content_type='application/json')
  if capacity < 0:
    return HttpResponse(Response(c=5, m="门店容量必须为正整数(人)").toJson(), content_type='application/json')
  # 创建新门店
  newShop = Shop(name=name, location=location, price=price, capacity=capacity, invalide_times=invalide_times)
  newShop.save()
  return HttpResponse(Response(m=newShop.id).toJson(), content_type='application/json')

# 删除门店对象
def deleteShop(shop):
  # 删除shop的所有time_bucket
  for tb in shop.time_bucket_set.all():
    tb.delete()
  # 删除shop的所有订单
  deleteOrders(shop.order_set.all())
  # 删除shop的所有课程
  for course in shop.course_set.all():
    course.delete()
  # 删除shop的所有服务
  for service in shop.service_set.all():
    service.delete()
  # 删除shop
  shop.delete()

# 删除指定门店信息
def delete(request):
  # 获取数据
  sid = request.POST.get('sid', None)
  # 判断数据有效性
  if sid is None:
    return HttpResponse(Response(c=-9, m='未提供sid').toJson(), content_type='application/json')
  try:
    sid = int(sid)
    deleteShop(Shop.objects.get(id=sid))
  except:
    return HttpResponse(Response(c=-3, m='指定删除门店不存在').toJson(), content_type='application/json')
  return HttpResponse(Response().toJson(), content_type='application/json')

# 更新指定门店信息
def update(request):
  # 获取数据
  name = request.POST.get('name', None)
  location = request.POST.get('location', None)
  price = request.POST.get('price', None)
  capacity = request.POST.get('capacity', None)
  sid = request.POST.get('sid', None)
  invalide_times = request.POST.get('invalide_times', None)
  shop = None
  # 判断数据正确性
  if sid is None:
    return HttpResponse(Response(c=-9, m='未提供sid').toJson(), content_type='application/json')
  try:
    shop = Shop.objects.get(id=int(sid))
  except:
    return HttpResponse(Response(c=-3, m='指定删除门店不存在').toJson(), content_type='application/json')
  if name is not None and len(name) > 50:
    return HttpResponse(Response(c=1, m="门店名称不得超过50字").toJson(), content_type='application/json')
  if location is not None and len(location) > 200:
    return HttpResponse(Response(c=2, m="地址长度不得超过200字").toJson(), content_type='application/json')
  if price is not None:
    try:
      price = int(price)
      if price < 0:
        return HttpResponse(Response(c=4, m="单价必须为正整数(元)").toJson(), content_type='application/json')
    except:
      return HttpResponse(Response(c=3, m="单价必须为数值").toJson(), content_type='application/json')
  if capacity is not None:
    try:
      capacity = int(capacity)
      if capacity < 0:
        return HttpResponse(Response(c=5, m="门店容量必须为正整数(人)").toJson(), content_type='application/json')
    except:
      return HttpResponse(Response(c=3, m="门店容量必须为数值").toJson(), content_type='application/json')
  # 更新门店信息
  shop.name = name if name is not None else shop.name
  shop.location = location if location is not None else shop.location
  shop.price = price if price is not None else shop.price
  shop.capacity = capacity if capacity is not None else shop.capacity
  shop.invalide_times = invalide_times if invalide_times is not None else shop.invalide_times
  shop.save()
  return HttpResponse(Response().toJson(), content_type='application/json')