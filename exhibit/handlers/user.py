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
from django.db.models import F

from holicLab.utils import *
from holicLab.models import Shop, Time_Bucket, Course, Service

# 显示用户的基本信息
def detail(request):
  user = User.objects.get(invite_code=request.session['user'])
  return render(request, 'exhibit/user.html', {'user' : user})

# 更新用户的基本信息
def update(request):
  if request.method == 'GET':
    raise Http404
  user = User.objects.get(invite_code=request.session['user'])
  # 更新昵称
  nickname = request.POST.get('nickname', None)
  if nickname is not None and len(nickname) > 100:
    return HttpResponse(Response(c=1, m="昵称必须小于100个字").toJson(), content_type="application/json")
  user.nickname = nickname if nickname is not None else user.nickname
  # 更新角色
  role = request.POST.get('role', None)
  if role is not None:
    try:
      role = int(role)
    except:
      return HttpResponse(Response(c=2, m="角色不合法").toJson(), content_type="application/json")
    if role not in [1, 2]:
      return HttpResponse(Response(c=2, m="角色不合法").toJson(), content_type="application/json")
    user.role = role
  # 绑定手机
  phone = request.POST.get('phone', None)
  code = request.POST.get('code', None)
  if phone is not None:
    verification_code = json.loads(request.session['verification_code'])
    if code is None or code != verification_code['code'] or phone != verification_code['phone']:
      return HttpResponse(Response(c=3, m="验证码错误").toJson(), content_type="application/json")
    del request.session['verification_code']
    user.phone = phone
    user.bind_date = datetime.datetime.utcnow().date()
  return HttpResponse(Response(m="用户资料修改成功").toJson(), content_type="application/json")

def verify(request):
  phone = request.POST.get('phone', None)
  if phone is None:
    return HttpResponse(Response(c=-9, m="未提供待验证手机号码").toJson(), content_type="application/json")
  # 随机生成一个验证码
  code = random_x_bit_code(4)
  res = json.loads(sendSMS(phone, code))
  if res['code'] != 0:
    return HttpResponse(Response(c=1, m="发送验证码失败，请检查手机号码是否正确，稍后重试").toJson(), content_type="application/json")
  # 将验证码以及生成验证码的时间存入session
  request.session['verification_code'] = json.dumps({'code' : code, 'create_time' : datetime.datetime.now(), 'phone' : phone})
  # 将验证码返回给前端
  return HttpResponse(Response(m=code).toJson(), content_type="application/json")

def showInvite(request):
  invite_code = request.session['user']
  return render(request, 'exhibit/invite_show.html', {'code' : request.session['user']})

def useInvite(request):
  invite_code = request.GET.get('code', None)
  if request.method == 'GET' and invite_code is None:
    return render(request, 'exhibit/invite_use.html')
  # 判断数据合法性
  invite_code = request.POST.get('code', None) if invite_code is None else invite_code
  if invite_code is None or len(invite_code) != 6:
    return HttpResponse(Response(c=-9, m="未提供待使用的邀请码").toJson(), content_type="application/json")
  # 获取当前用户
  user = request.session['user']
  user = User.objects.get(invite_code=user)
  # 判断用户是否已使用过邀请码
  if user.invited_by:
    return HttpResponse(Response(c=2, m="您已经使用过邀请码").toJson(), content_type="application/json")
  # 判断邀请码是否有效
  invite_user = None
  try:
    invite_user = User.objects.get(invite_code=invite_code)
  except:
    return HttpResponse(Response(c=3, m="邀请码无效").toJson(), content_type="application/json")
  # 更新邀请码用户的余额
  invite_user.balance = F('balance') + 30
  # 将邀请的用户和被邀请的用户进行绑定
  user.invited_by = invite_user
  # 更新被邀请用户的余额
  user.balance = F('balance') + 30
  return HttpResponse(Response(m="使用邀请码成功").toJson(), content_type="application/json")


