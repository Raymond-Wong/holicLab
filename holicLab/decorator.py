# -*- coding: utf-8 -*-
import sys
sys.path.append('..')
reload(sys)
sys.setdefaultencoding('utf-8')

from django.http import HttpResponse, HttpResponseRedirect
from utils import Response
from django.shortcuts import render, redirect

import exhibit.views
from models import User
from holicLab.utils import Response

def handler(view):
  def unKnownErr(request, *args, **kwargs):
    try:
      ret = view(request, *args, **kwargs)
      # 如果请求一个页面的时候发生了已知的错误，则跳转到错误页面
      print request.method, isinstance(ret, Response), ret['code']
      if request.method == 'GET' and isinstance(ret, Response) and ret['code'] != 0:
        return HttpResponse(Response(c=-2, m='/error?msg=%s' % ret['msg']).toJson(), content_type="application/json")
      # 否则没发生错误，则直接返回请求的内容
      return ret
    except Exception, e:
      info = sys.exc_info()
      print info
      info = str(info[1]).decode("unicode-escape")
      # 如果一个post请求发生了未知的错误，则告诉前端将页面跳转到错误页面
      if request.method == 'POST':
        return HttpResponse(Response(c=-2, m='/error?msg=%s' % info).toJson(), content_type="application/json")
      # 如果是一个get请求发生了为知的错误，则将页面重定向到错误情面
      return HttpResponseRedirect('/error?msg=%s' % info)
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
      # if request.method == 'POST':
      #   return HttpResponse(Response(c=-2, m='/user?action=verify&type=phone').toJson(), content_type="application/json")
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