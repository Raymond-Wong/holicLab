# -*- coding: utf-8 -*-
import sys
sys.path.append('..')
reload(sys)
sys.setdefaultencoding('utf-8')
import json
import markdown

from django.http import HttpResponse, HttpRequest, HttpResponseServerError, Http404
from django.shortcuts import render_to_response, redirect
from django.views.decorators.csrf import csrf_exempt

from holicLab.decorators import *

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
def CouponHandler(request):
  pass

