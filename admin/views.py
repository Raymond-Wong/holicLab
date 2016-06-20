# -*- coding: utf-8 -*-
import sys
sys.path.append('..')
reload(sys)
sys.setdefaultencoding('utf-8')
import json

from django.http import HttpResponse, HttpRequest, HttpResponseServerError, Http404
from django.shortcuts import render_to_response, redirect
from django.views.decorators.csrf import csrf_exempt

from holicLab.utils import *

from holicLab.decorator import *

ADMIN_NAME = 'holic'
ADMIN_PWD = 'holic'

# 登陆处理类
@csrf_exempt
@handler
def loginHandler(request):
  if request.method == 'GET':
    return render_to_response('/admin/login.html')
  else:
    username = request.POST.get('username', None)
    password = request.POST.get('password', None)
    if username != ADMIN_NAME:
      return HttpResponse(Response(m='账号错误', c=1).toJson(), content_type='application/json')
    elif password != ADMIN_PWD:
      return HttpResponse(Response(m='密码错误', c=2).toJson(), content_type='application/json')
    request.session['logined'] = True
    return HttpResponse(Response().toJson(), content_type='application/json')

# 登出处理类
@handler
@login_required
def logoutHandler(request):
  pass

# 商店的处理类
@handler
@login_required
def shopHandler(request):
  pass

# 课程的处理类
@handler
@login_required
def courseHandler(request):
  pass

# 密码处理类
@handler
@login_required
def passwordHandler(request):
  pass

# 会员处理类
@handler
@login_required
def memberHandler(request):
  pass

# 优惠券处理类
@handler
@login_required
def couponHandler(request):
  pass

# 订单处理类
@handler
@login_required
def orderHandler(request):
  pass