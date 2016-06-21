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
from holicLab.models import Shop

# 列出所有店铺
def list(request):
  shops = Shop.objects.all()
  return HttpResponse(Response(m=serializers.serialize("json", Shop.objects.all())).toJson(), content_type='application/json')

# 添加一个店铺
def add(request):
  # 获取数据
  name = request.POST.get('name', None)
  location = request.POST.get('location', None)
  price = request.POST.get('price', None)
  capacity = request.POST.get('capacity', None)
  # 判断数据有效性
  if name is None or location is None or price is None or capacity is None:
    return HttpResponse(Response(c=-9, m="为提供指定参数").toJson(), content_type='application/json')
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
  newShop = Shop(name=name, location=location, price=price, capacity=capacity)
  newShop.save()
  return HttpResponse(Response(m=newShop.id).toJson(), content_type='application/json')

# 删除指定门店信息
def delete(request):
  # 获取数据
  sid = request.POST.get('sid', None)
  # 判断数据有效性
  if sid is None:
    return HttpResponse(Response(c=-9, m='未提供sid').toJson(), content_type='application/json')
  try:
    sid = int(sid)
    Shop.objects.get(id=sid).delete()
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
  shop.save()
  return HttpResponse(Response().toJson(), content_type='application/json')