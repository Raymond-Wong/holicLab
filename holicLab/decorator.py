# -*- coding: utf-8 -*-
import sys
sys.path.append('..')
reload(sys)
sys.setdefaultencoding('utf-8')

from django.http import HttpResponse
from django.shortcuts import redirect
from utils import Response

import exhibit.views
from models import User

def handler(view):
  def unKnownErr(request, *args, **kwargs):
    try:
      return view(request, *args, **kwargs)
    except:
      info = sys.exc_info()
      info = str(info[1]).decode("unicode-escape")
      return HttpResponse(Response(c=-1, m=info).toJson(), content_type='application/json')
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
      request.session['backUrl'] = request.get_full_path()
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