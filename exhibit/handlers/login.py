# -*- coding: utf-8 -*-
import sys
sys.path.append('..')
reload(sys)
sys.setdefaultencoding('utf-8')
import json
from urllib import quote

from django.http import HttpResponse, HttpRequest, HttpResponseServerError, Http404
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers

import holicLab.settings as settings
from holicLab.utils import *
from holicLab.models import User

# nicely
# APP_ID = 'wx466a0c7c6871bc8e'
# APP_SECRET = 'aa06e2a00ce7dcae1d5e975e5217c478'
# holicLab
APP_ID = settings.WX_APP_ID
APP_SECRET = settings.WX_APP_SECRET
TOKEN = settings.WX_APP_TOKEN

def login(request, view):
  # 如果session中已经保存了用户信息，则不用重复获取用户信息
  if request.session.has_key('user'):
    print rmReArgs(request)
    return view(request)
  # 获取code
  code = request.GET.get('code', None)
  if code is None and request.method == 'GET':
    url = 'http://' + request.get_host() + request.get_full_path()
    url = quote(url, safe='')
    url = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=' + APP_ID + '&redirect_uri=' + url + '&response_type=code&scope=snsapi_userinfo&state=STATE#wechat_redirect'
    return redirect(url)
  # 用code换取access token
  params = {}
  params['appid'] = APP_ID
  params['secret'] = APP_SECRET
  params['code'] = code
  params['grant_type'] = 'authorization_code'
  res = send_request('api.weixin.qq.com', '/sns/oauth2/access_token', 'GET', params=params)
  if not res[0]:
    return HttpResponse(Response(c=1, m="login failed: get access token failed").toJson(), content_type='application/json')
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
    res = send_request('api.weixin.qq.com', '/sns/userinfo', 'GET', params=params)
    if not res[0]:
      return HttpResponse(Response(c=2, m="login failed: get user from wechat info failed").toJson(), content_type='application/json')
    userInfo = res[1]
    user = User()
    user.wx_openid = openid
    user.nickname = filterEmoji(userInfo['nickname'])
    user.gender = 'm' if userInfo['sex'] == 1 else 'f'
    user.invite_code = genInviteCodeRepeate()
    user.save()
    print 'openid: %s, nickname: %s, id: %s, invite_code: %s' % (openid, userInfo['nickname'], user.id, user.invite_code)
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

# 移除url中多余的参数
def rmReArgs(request):
  reArgs = ['code']
  prefix = request.get_full_path().split('?')[0]
  args = '?'.join(request.get_full_path().split('?')[1:]).split('&')
  needArgs = []
  for arg in args:
    key = arg.split('=')[0]
    if key not in reArgs:
      needArgs.append(arg)
  url = 'http://' + request.get_host() + prefix + '?' + '&'.join(needArgs)
  return url
