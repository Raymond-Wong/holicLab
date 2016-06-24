# -*- coding: utf-8 -*-
import sys
sys.path.append('..')
reload(sys)
sys.setdefaultencoding('utf-8')
import json
import time
import datetime

from django.http import HttpResponse, HttpRequest, HttpResponseServerError, Http404
from django.shortcuts import render_to_response, redirect
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers

from holicLab.utils import *
from holicLab.models import Course, Time_Bucket

from order import deleteOrders

# 展示课程
def list(request):
  # 检查数据合法性
  validate = isValidate(request, {'sid' : False}, False)
  if not validate[0]:
    return HttpResponse(validate[1], content_type='application/json')
  sid = request.POST.get('sid', None)
  shop = None
  courses = None
  if sid is not None:
    shop = Shop.objects.get(id=int(sid))
    courses = shop.course_set.all()
  else:
    courses = Course.objects.all()
  return HttpResponse(Response(m=serializers.serialize("json", courses)).toJson(), content_type='application/json')

# 添加课程
def add(request):
  # 检查数据合法性
  validate = isValidate(request, {}, True)
  if not validate[0]:
    return HttpResponse(validate[1], content_type='application/json')
  sid = int(request.POST.get(sid))
  name = request.POST.get('name')
  description = request.POST.get('description')
  start_time = datetime.datetime.strptime(request.POST.get('start_time'), '%Y-%m-%d %H:%M:%S')
  end_time = datetime.datetime.strptime(request.POST.get('end_time'), '%Y-%m-%d %H:%M:%S')
  tags = request.POST.get('tags')
  price = int(request.POST.get('price'))
  state = 1
  capacity = int(request.POST.get('capacity'))
  time_buckets = request.POST.get('time_buckets')
  newCourse = Course(name=name, description=description, tags=tags, price=price, state=state, capacity=capacity)
  newCourse.shop = Shop.objects.get(id=sid)
  newCourse.save()
  # 根据time_buckets创建该课程可预约时间
  # timebuckets的格式是[{date : , start_time: , end_time: }, ...]
  for time_bucket in time_buckets:
    date = datetime.datetime.strptime(time_bucket['date'], '%Y-%m-%d').date()
    start_time = time_bucket['start_time']
    end_time = time_bucket['end_time']
    occupation = {start_time + '-' + end_time : 0}
    ntb = Time_Bucket(date=date, occupation=json.dumps(occupation), course=course)
    ntb.save()
  return HttpResponse(Response(m=newCourse.id).toJson(), content_type='application/json')

# 删除课程
def delete(request):
  # 检查数据合法性
  validate = isValidate(request, {'cid' : True}, False)
  if not validate[0]:
    return HttpResponse(validate[1], content_type='application/json')
  cid = int(request.POST.get('cid'))
  course = Course.objects.get(id=cid)
  # 删除与该课程相关的所有订单
  deleteOrders(course.order_set.all())
  # 删除和该课程相关的所有时间
  for time_bucket in course.time_bucket_set.all():
    time_buckets.delete()
  # 删除该课程
  course.delete()
  return HttpResponse(Response().toJson(), content_type='application/json')

# 更新课程
def update(request):
  # 检查数据合法性
  validate = isValidate(request, {'cid' : True, 'sid' : False, 'time' : False}, True)
  if not validate[0]:
    return HttpResponse(validate[1], content_type='application/json')
  cid = int(request.POST.get('cid', None))
  course = Course.objects.get(id=cid)
  name = request.POST.get('name', None)
  course.name = name
  description = request.POST.get('description', None)
  course.description = description
  start_time = datetime.datetime.strptime(request.POST.get('start_time', None), '%Y-%m-%d %H:%M:%S')
  course.start_time = start_time
  end_time = datetime.datetime.strptime(request.POST.get('end_time', None), '%Y-%m-%d %H:%M:%S')
  course.end_time = end_time
  tags = request.POST.get('tags', None)
  course.tags = tags
  price = int(request.POST.get('price', None))
  course.price = price
  capacity = int(request.POST.get('capacity'))
  course.capacity = capacity
  return HttpResponse(Response().toJson(), content_type='application/json')

# 检查数据合法性
def isValidate(request, required, defaultRequired):
  # 补全required字典
  allKey = ['sid', 'name', 'description', 'time', 'tags', 'price', 'capacity', 'cid']
  for key in allKey:
    if not required.has_key(key):
      required[key] = defaultRequired
  # 判断sid合法性
  sid = request.POST.get('sid', None)
  if required['sid'] and sid is None:
    return (False, Response(c=-9, m='未提供商店id').toJson())
  try:
    if required['sid']:
      Shop.objects.get(id=int(sid))
  except:
    return (False, Response(c=-3, m='商店不存在').toJson())
  # 判断cid合法性
  cid = request.POST.get('cid', None)
  if required['cid'] and cid is None:
    return (False, Response(c=-9, m='未提供课程id').toJson())
  try:
    if required['cid']:
      Course.objects.get(id=int(cid))
  except:
    return (False, Response(c=-4, m='课程不存在').toJson())
  # 判断name合法性
  name = request.POST.get('name', None)
  if required['name'] and name is None:
    return (False, Response(c=-9, m='未提供课程名称').toJson())
  if required['name'] and len(name) > 50:
    return (False, Response(c=1, m='课程名称不得超过50字').toJson())
  # 判断description合法性
  description = request.POST.get('description', None)
  if required['description'] and description is None:
    return (False, Response(c=-9, m='未提供课程描述').toJson())
  # 判断开始时间和结束时间合法性
  time_buckets = request.POST.get('time_buckets', None)
  if required['time'] and time_buckets is None:
    return (False, Response(c=-9, m='未提供时间参数').toJson())
  # 判断标签
  tags = request.POST.get('tags', None)
  if required['tags'] and tags is None:
    return (False, Response(c=-9, m='未提供课程标签').toJson())
  # 判断价格合法性
  price = request.POST.get('price', None)
  if required['price'] and price is None:
    return (False, Response(c=-9, m='未提供课程价格').toJson())
  try:
    int(price)
  except:
    return (False, Response(c=3, m='课程价格必须为数值').toJson())
  # 判断容量合法性
  capacity = request.POST.get('capacity', None)
  if required['capacity'] and capacity is None:
    return (False, Response(c=-9, m='未提供课程容量').toJson())
  try:
    int(capacity)
  except:
    return (False, Response(c=5, m='课程容量必须为数值').toJson())
  return (True, None)