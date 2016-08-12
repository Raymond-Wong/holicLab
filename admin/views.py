# -*- coding: utf-8 -*-
import sys
sys.path.append('..')
reload(sys)
sys.setdefaultencoding('utf-8')
import json
import csv
import datetime
import time

from django.http import HttpResponse, HttpRequest, HttpResponseServerError, Http404
from django.shortcuts import render_to_response, redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from holicLab.utils import *
from holicLab.decorator import *
from holicLab.models import Image

import handlers.shop, handlers.course, handlers.member, handlers.order, handlers.coupon

ADMIN_NAME = md5('holic')
ADMIN_PWD = md5('holic8888Lab')

@handler
def indexHandler(request):
  return redirect('/admin/shop?action=list')

# 登陆处理类
@handler
def loginHandler(request):
  if request.method == 'GET':
    if request.session.has_key('logined') and request.session['logined']:
      return redirect('/admin/shop?action=list')
    return render(request,'admin/login.html')
  else:
    username = request.POST.get('account', None)
    password = request.POST.get('password', None)
    if username != ADMIN_NAME:
      return HttpResponse(Response(m='账号错误', c=1).toJson(), content_type='application/json')
    elif password != ADMIN_PWD:
      return HttpResponse(Response(m='密码错误', c=2).toJson(), content_type='application/json')
    request.session['logined'] = True
    return HttpResponse(Response(m='/admin/shop?action=list').toJson(), content_type='application/json')

# 登出处理类
@handler
@login_required
def logoutHandler(request):
  request.session.pop('logined')
  return redirect('/admin/login')

# 商店的处理类
@handler
@login_required
def shopHandler(request):
  action = request.GET.get('action', None)
  if action == 'list':
    return handlers.shop.list(request)
  elif action == 'add':
    return handlers.shop.add(request)
  elif action == 'delete':
    return handlers.shop.delete(request)
  elif action == 'update':
    return handlers.shop.update(request)
  elif action == 'release':
    return handlers.shop.release(request)
  elif action == 'get':
    return handlers.shop.get(request)
  elif action == 'calendar':
    return handlers.shop.calendar(request)
  return HttpResponse(Response(c=-8, m='操作类型错误').toJson(), content_type='application/json')

# 课程的处理类
@login_required
def courseHandler(request):
  action = request.GET.get('action', None)
  if action == 'list':
    return handlers.course.list(request)
  elif action == 'add':
    return handlers.course.add(request)
  elif action == 'delete':
    return handlers.course.delete(request)
  elif action == 'update':
    return handlers.course.update(request)
  elif action == 'release':
    return handlers.course.release(request)
  elif action == 'get':
    return handlers.course.get(request)
  elif action == 'calendar':
    return handlers.course.calendar(request)
  return HttpResponse(Response(c=-8, m='操作类型错误').toJson(), content_type='application/json')

# 会员处理类
@handler
@login_required
def memberHandler(request):
  action = request.GET.get('action', None)
  if action == 'list':
    return handlers.member.list(request)
  return HttpResponse(Response(c=-8, m='操作类型错误').toJson(), content_type='application/json')

# 订单处理类
@handler
@login_required
def orderHandler(request):
  action = request.GET.get('action', None)
  if action == 'list':
    return handlers.order.list(request)
  return HttpResponse(Response(c=-8, m='操作类型错误').toJson(), content_type='application/json')

# 优惠券处理类
@handler
@login_required
def couponHandler(request):
  action = request.GET.get('action', None)
  if action == 'list':
    return handlers.coupon.list(request)
  return HttpResponse(Response(c=-8, m='操作类型错误').toJson(), content_type='application/json')

# 导出表格处理类
@handler
@login_required
def exportHandler(request):
  # 检查数据合法性
  th = request.POST.get('th', None)
  trs = request.POST.get('trs', None)
  for tr in trs:
    if len(tr) != len(th):
      return HttpResponse(Response(c=1, m='表格格式错误').toJson(), content_type='application/json')
  # 生成csv
  response = HttpResponse(mimetype='text/csv')
  response['Content‐Disposition'] = 'attachment; filename=%s.csv' % str(int(time.time()))
  # 往csv中填充内容
  writer = csv.writer(response)
  writer.writerow(th)
  for tr in trs:
    writer.writerow(tr)
  return reponse

# 上传图片
@csrf_exempt
@handler
@login_required
def uploadHandler(request):
  image = request.FILES['image']
  image._name = '%s_%s' % (str(int(time.time())), image._name)
  image = Image(url=image)
  image.save()
  url = appendImageUrl(image.__dict__.get('url'))
  return HttpResponse(Response(m=url).toJson(), content_type='application/json')