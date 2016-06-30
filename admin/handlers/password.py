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
from holicLab.models import Password

# 列出所有密码
def list(request):
  if request.method == 'GET':
    return render_to_response('admin/password.html', {'activePage' : 'password', 'passwords' : Password.objects.all()})
  start_time = request.POST.get('start_time', None)
  end_time = request.POST.get('end_time', None)
  sid = request.POST.get('sid', None)
  shop = None
  # 检查数据合法性
  try:
    if start_time is not None:
      start_time = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
    if end_time is not None:
      end_time = datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
  except:
    return HttpResponse(Response(c=-10, m='时间格式错误(年-月-日 时:分:秒)').toJson(), content_type='application/json')
  try:
    shop = Shop.objects.get(id=int(sid))
  except:
    return HttpResponse(Response(c=-3, m='商店不存在').toJson(), content_type='application/json')
  # 如果没有提供开始时间则从2000年开始,没有提供结束时间则为当前时间
  start_time = start_time if start_time is not None else datetime.datetime.strptime('2000-1-1 0:0:0', '%Y-%m-%d %H:%M:%S')
  end_time = end_time if end_time is not None else datetime.datetime.now()
  # 根据时间段获取密码
  passwords = shop.order_set.filter(create_time__gte=start_time).filter(create_time__lt=end_time).password_set.all()
  return HttpResponse(Response(m=serializers.serialize("json", passwords)).toJson(), content_type='application/json')

def add(request):
  pass

def delete(request):
  pass

def assign(request):
  pass