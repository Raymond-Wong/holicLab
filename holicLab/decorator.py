# -*- coding: utf-8 -*-
import sys
sys.path.append('..')
reload(sys)
sys.setdefaultencoding('utf-8')
import traceback
import random
import time

from django.http import HttpResponse, HttpResponseRedirect
from utils import Response
from django.shortcuts import render, redirect

import exhibit.views
from models import User
from holicLab.utils import Response

def handler(view):
  def unKnownErr(request, *args, **kwargs):
    try:
      return view(request, *args, **kwargs)
    except Exception, e:
      errId = '%s.%s' % (str(time.time()), str(random.randint(0, 1000)))
      print '*' * 10, 'errid:', errId, '*' * 10
      traceback.print_exc()
      print '*' * 10, 'endof:', errId, '*' * 10
      info = sys.exc_info()
      info = str(info[1]).decode("unicode-escape")
      # 如果一个post请求发生了未知的错误，则告诉前端将页面跳转到错误页面
      if request.method == 'POST':
        return HttpResponse(Response(c=-2, m='/error?msg=%s' % errId).toJson(), content_type="application/json")
      # 如果是一个get请求发生了为知的错误，则将页面重定向到错误情面
      return HttpResponseRedirect('/error?msg=%s' % errId)
  return unKnownErr

def login_required(view):
  def verified(request, *args, **kwargs):
    if request.session.has_key('logined') and request.session['logined']:
      return view(request, *args, **kwargs)
    return redirect('/admin/login')
  return verified

def verify_required(view):
  def verified(request, *args, **kwargs):
    user = User.objects.get(invite_code=request.session['user'])
    if user.phone == None or len(user.phone) == 0:
      if request.method == 'GET':
        request.session['backUrl'] = request.get_full_path()
      else:
        request.session['backUrl'] = '/'
        # 如果是post请求的话则要告诉前端进行跳转
        return HttpResponse(Response(c=-2, m='/user?action=verify&type=phone').toJson(), content_type="application/json")
      return redirect('/user?action=verify&type=phone')
    return view(request, *args, **kwargs)
  return verified
# def verify_required(view):
#   def verified(request, *args, **kwargs):
#     return view(request, *args, **kwargs)
#   return verified

def wx_logined(view):
  def verified(request, *args, **kwargs):
    if request.session.has_key('user'):
      return view(request, *args, **kwargs)
    return exhibit.views.loginHandler(request, view, *args, **kwargs)
  return verified
# def wx_logined(view):
#   def verified(request, *args, **kwargs):
#     return view(request, *args, **kwargs)
#   return verified