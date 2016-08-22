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
from django.utils import timezone

from holicLab.utils import *
from holicLab.models import Shop, Time_Bucket, Course, Service

# 列出所有店铺
def list(request):
  sid = request.GET.get('sid', None)
  shop = None
  # 判断sid合法性
  if sid is None:
    return HttpResponse(Response(c=-9, m="未提供sid").toJson(), content_type="application/json")
  try:
    shop = Shop.objects.get(id=int(sid))
  except Exception, e:
    return HttpResponse(Response(c=-3, m="待查询商店不存在").toJson(), content_type="application/json")
  courses = shop.course_set.all()
  # 将图片列表从字符串处理成数组
  for course in courses:
    course.cover = json.loads(course.cover)
  return render(request, 'exhibit/course_list.html', {'courses' : courses})

# 显示商店详情
def detail(request):
  cid = request.GET.get('cid', None)
  course = None
  # 判断cid合法性
  if cid is None:
    return HttpResponse(Response(c=-9, m="未提供cid").toJson(), content_type="application/json")
  try:
    course = Course.objects.get(id=int(cid))
  except Exception, e:
    return HttpResponse(Response(c=-4, m="待查询课程不存在").toJson(), content_type="application/json")
  course.cover = json.loads(course.cover)
  times = []
  bookable_time_records = course.bookable_time_set.filter(start_time__gte=timezone.now()).filter(occupation__lt=course.capacity)
  for i, time in enumerate(bookable_time_records):
    times.append({'id' : time.id, 'startTime' : time.start_time, 'endTime' : time.end_time, 'occupation' : time.occupation})
  course.bookable_time = json.dumps(times, cls=MyJsonEncoder)
  # 设置课程价格为单位元
  course.price = course.price / 10.0
  # 返回商店详情
  return render(request, 'exhibit/course_detail.html', {'course' : course})
