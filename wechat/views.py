# -*- coding: utf-8 -*-
import sys
sys.path.append('..')
reload(sys)
sys.setdefaultencoding('utf-8')

import hashlib
import time
import json
try: 
  import xml.etree.cElementTree as ET
except ImportError: 
  import xml.etree.ElementTree as ET

from datetime import datetime, timedelta
from django.utils.encoding import smart_str
from django.utils import timezone

from django.http import HttpResponse, HttpRequest, HttpResponseServerError, Http404
from django.shortcuts import render_to_response, redirect
from django.views.decorators.csrf import csrf_exempt

# 服务号
APPID = 'wx466a0c7c6871bc8e'
APPSECRET = 'aa06e2a00ce7dcae1d5e975e5217c478'
TOKEN = 'holicLab'

@csrf_exempt
def entrance(request):
  if request.method == 'GET':
    if verify(TOKEN, request.GET.get('timestamp', None), request.GET.get('nonce', None), request.GET.get('signature', None)):
      update_token()
      return HttpResponse(request.GET.get('echostr', None))
    else:
      return HttpResponse('forbiden from browswer')
  raise Http404

# 验证信息是否从微信发送过来
def verify(token, timestamp, nonce, signature):
  tmpList = [token, timestamp, nonce]
  tmpList.sort()
  tmpStr = '%s%s%s' % tuple(tmpList)
  tmpStr = hashlib.sha1(tmpStr).hexdigest()
  return tmpStr == signature

# 当数据库中access_token失效以后用于更新token的接口
def update_token():
  params = {
    'grant_type': 'client_credential',
    'appid': APPID,
    'secret': APPSECRET
  }
  host = 'api.weixin.qq.com'
  path = '/cgi-bin/token'
  method = 'GET'
 
  res = holicLab.utils.send_request(host, path, method, params=params)
  if not res[0]:
    return False
  if res[1].get('errcode'):
    return False
  token = res[1].get('access_token')
  starttime = timezone.now()
  expires_in = timedelta(seconds=int(res[1].get('expires_in')))
  endtime = starttime + expires_in
  token_record = Ticket.objects.filder(ticket_type=1).order_by('-start_time')
  if len(token_record) > 0:
    token_record = token_record[0]
  else:
    token_record = access_token()
  token_record.content = token
  token_record.end_time = endtime
  token_record.save()
  return token_record