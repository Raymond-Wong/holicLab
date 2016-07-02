# -*- coding: utf-8 -*-
import sys
sys.path.append('..')
reload(sys)
sys.setdefaultencoding('utf-8')
import json
import markdown

from django.http import HttpResponse, HttpRequest, HttpResponseServerError, Http404
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from holicLab.decorators import *
import handlers.shop

# 商店的处理类
@handler
@login_required
def shopHandler(request):
  action = request.GET.get('action')
  if action == 'list':
    return handlers.shop.list(request)
  elif action == 'detail':
    return handlers.shop.detail(request)
  return HttpResponse(Response(c=-8, m='操作类型错误').toJson(), content_type='application/json')

# 课程的处理类
@handler
@login_required
def courseHandler(request):
  pass