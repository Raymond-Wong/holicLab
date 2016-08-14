# -*- coding: utf-8 -*-
import sys
sys.path.append('..')
reload(sys)
sys.setdefaultencoding('utf-8')
import json

from django.http import HttpResponse, HttpRequest, HttpResponseServerError, Http404
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers

from holicLab.utils import *
from holicLab.models import Shop, Time_Bucket, Course, Service

from order import deleteOrders

# 列出所有店铺
def list(request):
  unreleasedShop = Shop.objects.filter(state=1)
  releasedShop = Shop.objects.filter(state=2)
  hasShop = True if len(unreleasedShop) + len(releasedShop) > 0 else False
  # 将图片列表从字符串处理成数组
  for shop in unreleasedShop:
    shop.cover = json.loads(shop.cover)
  for shop in releasedShop:
    shop.cover = json.loads(shop.cover)
  return render(request, 'admin/shop_list.html', {'activePage' : 'content', 'unreleasedShops' : unreleasedShop, 'releasedShops' : releasedShop, 'hasShop' : hasShop})

# 添加一个店铺
def add(request):
  if request.method == 'GET':
    return render(request, 'admin/shop_add.html', {'activePage' : 'content'})
  # 获取数据
  name = request.POST.get('name', None)
  cover_type = request.POST.get('cover_type', None);
  cover = request.POST.get('cover', None);
  description = request.POST.get('description', None);
  location = request.POST.get('location', None)
  price = request.POST.get('price', None)
  capacity = request.POST.get('capacity', None)
  notice = request.POST.get('notice', None);
  invalide_times = request.POST.get('invalide_times', [])
  phone = request.POST.get('phone', None)
  password = request.POST.get('password', None)
  # 判断数据有效性
  if name is None or location is None or price is None or capacity is None or invalide_times is None or cover_type is None or cover is None or description is None:
    return HttpResponse(Response(c=-9, m="未提供指定参数").toJson(), content_type='application/json')
  if len(name) > 50:
    return HttpResponse(Response(c=1, m="门店名称不得超过50字").toJson(), content_type='application/json')
  if len(location) > 200:
    return HttpResponse(Response(c=2, m="地址长度不得超过200字").toJson(), content_type='application/json')
  # if len(phone) > 12:
  #   return HttpResponse(Response(c=3, m="电话长度不得超过12字").toJson(), content_type='application/json')
  if len(password) != 6:
    return HttpResponse(Response(c=4, m="场地密码长度必须为6位").toJson(), content_type='application/json')
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
  newShop = Shop(password=password, phone=phone, name=name, location=location, price=price, capacity=capacity, invalide_times=invalide_times, description=description, cover=cover, cover_type=cover_type, notice=notice)
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
  shop = None
  # 判断数据有效性
  if sid is None:
    return HttpResponse(Response(c=-9, m='未提供sid').toJson(), content_type='application/json')
  try:
    sid = int(sid)
    shop = Shop.objects.get(id=sid)
  except Exception, e:
    return HttpResponse(Response(c=-3, m='指定删除门店不存在').toJson(), content_type='application/json')
  deleteShop(shop)
  return HttpResponse(Response().toJson(), content_type='application/json')

# 更新指定门店信息
def update(request):
  if request.method == 'GET':
    sid = request.GET.get('sid', None)
    return render(request, 'admin/shop_update.html', {'activePage' : 'content', "shop" : Shop.objects.get(id=sid)})
  # 获取数据
  name = request.POST.get('name', None)
  location = request.POST.get('location', None)
  price = request.POST.get('price', None)
  capacity = request.POST.get('capacity', None)
  sid = request.POST.get('sid', None)
  invalide_times = request.POST.get('invalide_times', [])
  cover = request.POST.get('cover', None)
  cover_type = request.POST.get('cover_type', None)
  notice = request.POST.get('notice', None)
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
  shop.cover = cover if cover is not None else shop.cover
  shop.cover_type = cover_type if cover_type is not None else shop.cover_type
  shop.notice = notice if notice is not None else shop.notice
  shop.save()
  return HttpResponse(Response().toJson(), content_type='application/json')

def release(request):
  # 获取数据
  sid = request.POST.get('sid', None)
  shop = None
  # 判断数据有效性
  if sid is None:
    return HttpResponse(Response(c=-9, m='未提供sid').toJson(), content_type='application/json')
  try:
    sid = int(sid)
    shop = Shop.objects.get(id=sid)
  except Exception, e:
    return HttpResponse(Response(c=-3, m='指定删除门店不存在').toJson(), content_type='application/json')
  shop.state = 2
  shop.releaseDate = timezone.now().date()
  shop.save()
  return HttpResponse(Response(m='发布成功').toJson(), content_type='application/json')

def get(request):
  # 获取数据
  sid = request.POST.get('sid', None)
  shop = None
  # 判断数据有效性
  if sid is None:
    return HttpResponse(Response(c=-9, m='未提供sid').toJson(), content_type='application/json')
  try:
    sid = int(sid)
    shop = Shop.objects.get(id=sid)
  except Exception, e:
    return HttpResponse(Response(c=-3, m='指定删除门店不存在').toJson(), content_type='application/json')
  return HttpResponse(Response(m=shop.toJSON()).toJson(), content_type='application/json')

def calendar(request):
  if request.method == 'GET':
    shop = Shop.objects.get(id=request.GET.get('sid'))
    return render(request, 'admin/shop_calendar.html', {'activePage' : 'content', 'shop' : shop})
  raise Http404
