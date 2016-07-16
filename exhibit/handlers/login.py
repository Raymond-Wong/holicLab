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

from holicLab.utils import *

APP_ID = 'wx466a0c7c6871bc8e'
APP_SECRET = 'aa06e2a00ce7dcae1d5e975e5217c478'
TOKEN = 'holicLab'

def login(request, view):
  # 如果session中已经保存了用户信息，则不用重复获取用户信息
  if request.session.has_key('user'):
    return view(request)
  # 获取code
  code = request.GET.get('code')
  # 用code换取access token
  params = {}
  params['appid'] = APP_ID
  params['secret'] = APP_SECRET
  params['code'] = code
  params['grant_type'] = 'authorization_code'
  res = send_request('api.weixin.qq.com', '/sns/oauth2/access_token', 'GET', params=params)
  if not res[0]:
    return HttpResponse(Response(c=1, m="登陆失败: 获取access token失败").toJson(), content_type='application/json')
  access_token = res[1]['access_token']
  openid = res[1]['openid']
  # 获取用户
  user = None
  try:
    # 用户存在数据库中
    user = User.objects.get(wx_openid=str(openid))
  except:
    # 用户不存在数据库中
    params = {}
    params['access_token'] = access_token
    params['openid'] = openid
    params['lang'] = 'zh_CN'
    print params
    res = send_request('api.weixin.qq.com', '/sns/userinfo/', 'GET', params=params)
    print res
    if not res[0]:
      return HttpResponse(Response(c=2, m="登陆失败: 获取用户身份失败").toJson(), content_type='application/json')
    userInfo = res[1]
    user = User()
    user.wx_openid = openid
    user.nickname = userInfo['nickname']
    user.gender = 'm' if userInfo['gender'] == '1' else 'f'
    user.invite_code = genInviteCodeRepeate()
    user.save()
  request.session['user'] = user.invite_code
  return view(request)

# 重复生成随机六位的邀请码，直至生成一个不在数据库中存在的邀请码为至
def genInviteCodeRepeate():
  code = random_x_bit_code(6)
  try:
    User.objects.get(invite_code=code)
  except:
    return code
  return genInviteCodeRepeate()