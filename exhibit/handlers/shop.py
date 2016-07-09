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
  # 返回商店详情
  return render(request, 'exhibit/shop_detail.html', {'shop' : shop})
