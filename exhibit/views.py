# -*- coding: utf-8 -*-
import sys
sys.path.append('..')
reload(sys)
sys.setdefaultencoding('utf-8')
import json

from django.http import HttpResponse, HttpRequest, HttpResponseServerError, Http404
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from holicLab.decorator import *
from holicLab.models import *
import handlers.shop, handlers.course, handlers.user, handlers.login, handlers.order, handlers.pay, handlers.notify

def testHandler(request):
  return render(request, 'exhibit/user_tags.html')

# 错误提示类
def errorHandler(request):
  msg = request.GET.get('msg', '未获取错误信息')
  time = timezone.now()
  return render(request, 'exhibit/error.html', {'msg' : msg, 'time' : time})

# 微信端入口
@handler
def loginHandler(request, view):
  return handlers.login.login(request, view)

# 首页的处理类
@handler
@wx_logined
def homeHandler(request):
  shops = Shop.objects.filter(state=2)[:2]
  now = timezone.now()
  for shop in shops:
    shop.cover = json.loads(shop.cover)
    shop.courses = []
    courses = shop.course_set.filter(state=2).all()
    for i, course in enumerate(courses):
      course.cover = json.loads(course.cover)
      course.bookable_time = course.bookable_time_set.order_by('start_time')
      if len(course.bookable_time) > 0:
        course.bookable_time = course.bookable_time[0]
        shop.courses.append(course)
    shop.courses = sorted(shop.courses, cmp=lambda x, y:cmp(x.bookable_time.start_time, y.bookable_time.start_time))[:3]
  shops = shops[:1]
  return render(request, 'exhibit/home.html', {'shops' : shops, 'shopSize' : len(shops)})

# 商店的处理类
@handler
@wx_logined
def shopHandler(request):
  action = request.GET.get('action')
  if action == 'list':
    return handlers.shop.list(request)
  elif action == 'detail':
    return handlers.shop.detail(request)
  return HttpResponse(Response(c=-8, m='操作类型错误').toJson(), content_type='application/json')

# 课程的处理类
@handler
@wx_logined
def courseHandler(request):
  action = request.GET.get('action')
  if action == 'list':
    return handlers.course.list(request)
  elif action == 'detail':
    return handlers.course.detail(request)
  return HttpResponse(Response(c=-8, m='操作类型错误').toJson(), content_type='application/json')

# 用户的处理类
@handler
@wx_logined
def userHandler(request):
  action = request.GET.get('action', None)
  if action == 'detail':
    return handlers.user.detail(request)
  elif action == 'update':
    return handlers.user.update(request)
  elif action == 'verify':
    return handlers.user.verify(request)
  elif action == 'invite':
    return handlers.user.invite(request)
  return HttpResponse(Response(c=-8, m='操作类型错误').toJson(), content_type='application/json')

# 订单的处理类
@handler
@wx_logined
@verify_required
def orderHandler(request):
  action = request.GET.get('action', None)
  if action == 'list':
    return handlers.order.list(request)
  elif action == 'update':
    return handlers.order.update(request)
  elif action == 'get':
    return handlers.order.get(request)
  elif action == 'password':
    return handlers.order.password(request)
  elif action == 'refund':
    return handlers.order.refund(request)
  elif action == 'success':
    return handlers.order.success(request)
  # elif action == 'getRefundMoney':
  #   return handlers.order.getRefundMoney(request)
  return HttpResponse(Response(c=-8, m='操作类型错误').toJson(), content_type='application/json')

# 支付的处理类
@handler
@wx_logined
@verify_required
def payHandler(request):
  action = request.GET.get('action', None)
  if action == 'add':
    return handlers.pay.add(request)
  elif action == 'pre':
    return handlers.pay.pre(request)
  elif action == 'price':
    return handlers.pay.price(request)
  elif action == 'check':
    return handlers.pay.check(request)
  elif action == 'cancel':
    return handlers.pay.cancel(request)
  return HttpResponse(Response(c=-8, m='操作类型错误').toJson(), content_type='application/json')

# 付款结果通知的处理类
@csrf_exempt
def notifyHandler(request):
  return handlers.notify.notify(request)