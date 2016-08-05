# -*- coding: utf-8 -*-
import sys
sys.path.append('..')
reload(sys)
sys.setdefaultencoding('utf-8')
import json
import datetime

from django.http import HttpResponse, HttpRequest, HttpResponseServerError, Http404
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers

from holicLab.utils import *
from holicLab.models import Shop, Time_Bucket, Course, Service

# 列出所有店铺
def list(request):
  shops = Shop.objects.filter(state=2)
  # 将图片列表从字符串处理成数组
  for shop in shops:
    shop.cover = json.loads(shop.cover)
  return render(request, 'exhibit/shop_list.html', {'shops' : shops})

# 显示商店详情
def detail(request):
  sid = request.GET.get('sid', None)
  shop = None
  # 判断sid合法性
  if sid is None:
    return HttpResponse(Response(c=-9, m="未提供sid").toJson(), content_type="application/json")
  try:
    shop = Shop.objects.get(id=int(sid))
  except Exception, e:
    return HttpResponse(Response(c=-3, m="待查询商店不存在").toJson(), content_type="application/json")
  shop.cover = json.loads(shop.cover)
  shop.courses = shop.course_set.filter(state=2)
  for i, course in enumerate(shop.courses):
    shop.courses[i].cover = json.loads(shop.courses[i].cover)
    shop.courses[i].bookable_time = shop.courses[i].bookable_time_set.order_by('-start_time')[0]
  # 根据预约情况设置不可预约时间
  shop.invalide_times = json.loads(shop.invalide_times)
  for tb in shop.time_bucket_set.filter(start_time__gt=timezone.now()).filter(occupation__gte=shop.capacity):
    shop.invalide_times.append({'startTime' : tb.start_time, 'endTime' : tb.startTime + datetime.timedelta(seconds=60*30)})
  shop.invalide_times = json.dumps(shop.invalide_times, cls=MyJsonEncoder)
  # 返回商店详情
  return render(request, 'exhibit/shop_detail.html', {'shop' : shop})
