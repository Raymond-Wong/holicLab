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
from holicLab.models import Course, Bookable_Time, Shop

from order import deleteOrders

# 展示课程
def list(request):
  if request.method == 'GET':
    sid = request.GET.get('sid', None)
    if sid is None:
      unreleasedShop = Shop.objects.filter(state=1)
      releasedShop = Shop.objects.filter(state=2)
      hasShop = True if len(unreleasedShop) + len(releasedShop) > 0 else False
      # 将图片列表从字符串处理成数组
      for shop in unreleasedShop:
        shop.cover = json.loads(shop.cover)
      for shop in releasedShop:
        shop.cover = json.loads(shop.cover)
      return render_to_response('admin/course_shop_list.html', {'unreleasedShops' : unreleasedShop, 'releasedShops' : releasedShop, 'hasShop' : hasShop})
    else:
      shop = None
      try:
        sid = request.GET.get('sid', None)
        shop = Shop.objects.get(id=int(sid))
      except:
        return HttpResponse(Response(c=-3, m='待查询商店不存在').toJson(), content_type='application/json')
      unreleasedCourses = shop.course_set.filter(state=1)
      releasedCourses = shop.course_set.filter(state=2)
      for course in unreleasedCourses:
        course.cover = json.loads(course.cover)
      for course in releasedCourses:
        course.cover = json.loads(course.cover)
      return render_to_response('admin/course_list.html', {'sid' : sid, 'releasedCourses' : releasedCourses, 'unreleasedCourses' : unreleasedCourses})
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
  if request.method == 'GET':
    sid = request.GET.get('sid', None)
    try:
      shop = Shop.objects.get(id=int(sid))
    except:
      return HttpResponse(Response(c=-3, m="场地不存在").toJson, content_type="application/json")
    return render_to_response('admin/course_add.html', {'sid' : sid})
  # 检查数据合法性
  validate = isValidate(request, {'sid' : False}, True)
  if not validate[0]:
    return HttpResponse(validate[1], content_type='application/json')
  sid = int(request.GET.get('sid'))
  name = request.POST.get('name', None)
  cover_type = request.POST.get('cover_type', None);
  cover = request.POST.get('cover', None);
  description = request.POST.get('description', None);
  coach_description = request.POST.get('coach_description', None)
  coach_cover = request.POST.get('coach_cover', None)
  price = request.POST.get('price', None)
  capacity = request.POST.get('capacity', None)
  notice = request.POST.get('notice', None);
  time_buckets = json.loads(request.POST.get('bookable_time', '[]'))
  newCourse = Course(name=name, description=description, notice=notice, cover_type=cover_type, cover=cover, coach_description=coach_description, coach_cover=coach_cover, price=price, capacity=capacity)
  newCourse.shop = Shop.objects.get(id=sid)
  newCourse.save()
  # 根据time_buckets创建该课程可预约时间
  # timebuckets的格式是[{start_time: , end_time: }, ...]
  for time_bucket in time_buckets:
    start_time = time_bucket['startTime']
    end_time = time_bucket['endTime']
    ntb = Bookable_Time(start_time=start_time, end_time=end_time, course=newCourse)
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
  if request.method == 'GET':
    cid = request.GET.get('cid', None)
    return render_to_response('admin/course_update.html', {'course' : Course.objects.get(id=int(cid))})
  # 检查数据合法性
  validate = isValidate(request, {'sid' : False}, True)
  if not validate[0]:
    return HttpResponse(validate[1], content_type='application/json')
  cid = int(request.POST.get('cid', None))
  course = Course.objects.get(id=cid)
  name = request.POST.get('name', None)
  course.name = name
  description = request.POST.get('description', None)
  course.description = description
  price = int(request.POST.get('price', None))
  course.price = price
  capacity = int(request.POST.get('capacity'))
  course.capacity = capacity
  course.cover = request.POST.get('cover')
  course.cover_type = request.POST.get('cover_type')
  course.notice = request.POST.get('notice')
  course.coach_description = request.POST.get('coach_description')
  course.coach_cover = request.POST.get('coach_cover')
  bookable_time = json.loads(request.POST.get('bookable_time'))
  for time in bookable_time:
    timeRecord = None
    if time.has_key('tid'):
      timeRecord = Bookable_Time.objects.get(id=int(time['tid']))
      timeRecord.start_time = time['startTime']
      timeRecord.end_time = time['endTime']
    else:
      timeRecord = Bookable_Time.objects.create(course=course, start_time=time['startTime'], end_time=time['endTime'])
    timeRecord.save()
  course.save()
  return HttpResponse(Response().toJson(), content_type='application/json')

def release(request):
  # 获取数据
  cid = request.POST.get('cid', None)
  course = None
  # 判断数据有效性
  if cid is None:
    return HttpResponse(Response(c=-9, m='未提供cid').toJson(), content_type='application/json')
  try:
    cid = int(cid)
    course = Course.objects.get(id=cid)
  except Exception, e:
    return HttpResponse(Response(c=-4, m='指定删除课程不存在').toJson(), content_type='application/json')
  course.state = 2
  course.save()
  return HttpResponse(Response(m='发布成功').toJson(), content_type='application/json')

def get(request):
  # 获取数据
  cid = request.POST.get('cid', None)
  course = None
  # 判断数据有效性
  if cid is None:
    return HttpResponse(Response(c=-9, m='未提供cid').toJson(), content_type='application/json')
  try:
    cid = int(cid)
    course = Course.objects.get(id=cid)
  except Exception, e:
    return HttpResponse(Response(c=-4, m='指定删除课程不存在').toJson(), content_type='application/json')
  courseDict = json.loads(course.toJSON())
  courseDict['bookable_time'] = []
  for time in course.bookable_time_set.all():
    courseDict['bookable_time'].append(json.loads(time.toJSON()))
  return HttpResponse(Response(m=json.dumps(courseDict)).toJson(), content_type='application/json')

# 检查数据合法性
def isValidate(request, required, defaultRequired):
  # 补全required字典
  allKey = ['sid', 'name', 'description', 'time', 'coach_description', 'coach_cover', 'cover', 'cover_type', 'price', 'capacity']
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
  time_buckets = request.POST.get('bookable_time', [])
  if required['time'] and time_buckets is None:
    return (False, Response(c=-9, m='未提供时间参数').toJson())
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