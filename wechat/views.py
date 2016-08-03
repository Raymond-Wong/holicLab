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

from django.http import HttpResponse, HttpRequest, HttpResponseServerError, Http404
from django.shortcuts import render_to_response, redirect
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

import holicLab.settings as settings
from holicLab.utils import *
from models import Ticket

# nicely
# APPID = 'wx466a0c7c6871bc8e'
# APPSECRET = 'aa06e2a00ce7dcae1d5e975e5217c478'
# holicLab
APPID = settings.WX_APP_ID
APPSECRET = settings.WX_APP_SECRET
TOKEN = settings.WX_APP_TOKEN

@csrf_exempt
def entrance(request):
  if request.method == 'GET':
    if verify(TOKEN, request.GET.get('timestamp', None), request.GET.get('nonce', None), request.GET.get('signature', None)):
      update_token()
      return HttpResponse(request.GET.get('echostr', None))
    else:
      return HttpResponse('forbiden from browswer')
  raise Http404

def config(request):
  params = {}
  params['noncestr'] = random_x_bit_code(10)
  params['jsapi_ticket'] = get_ticket(2).content
  params['timestamp'] = str(int(time.time()))
  params['url'] = request.POST.get('url')
  toSignStr = '&'.join(map(lambda x:x[0] + '=' + x[1], sorted(params.iteritems(), lambda x,y:cmp(x[0], y[0]))))
  ret = {}
  ret['signature'] = sha1(toSignStr)
  ret['timestamp'] = params['timestamp']
  ret['noncestr'] = params['noncestr']
  ret['appId'] = APPID
  return HttpResponse(Response(m=ret).toJson(), content_type='application/json')

# 获取某种类型的ticket，1为access token，2为jsapi
def get_ticket(ticket_type):
  records = Ticket.objects.filter(ticket_type=ticket_type)
  toRefresh = True
  if len(records) > 0:
    record = records.order_by('-start_time')[0]
    if (timezone.now() - record.start_time).seconds < 7200:
      toRefresh = False
      print timezone.now(), record.start_time, (timezone.now() - record.start_time), (timezone.now() - record.start_time).seconds
  if toRefresh:
    record = update_token() if ticket_type == 1 else update_jsapi()
  return record

# 验证信息是否从微信发送过来
def verify(token, timestamp, nonce, signature):
  tmpList = [token, timestamp, nonce]
  tmpList.sort()
  tmpStr = '%s%s%s' % tuple(tmpList)
  tmpStr = hashlib.sha1(tmpStr).hexdigest()
  return tmpStr == signature

# 当数据库中access_token失效以后用于更新token的接口
def update_token():
  print 'update access token'
  params = {
    'grant_type': 'client_credential',
    'appid': APPID,
    'secret': APPSECRET
  }
  host = 'api.weixin.qq.com'
  path = '/cgi-bin/token'
  method = 'GET'
 
  res = send_request(host, path, method, params=params)
  if not res[0]:
    return False
  if res[1].get('errcode'):
    return False
  token = res[1].get('access_token')
  starttime = timezone.now()
  expires_in = timedelta(seconds=int(res[1].get('expires_in')))
  endtime = starttime + expires_in
  token_record = Ticket.objects.filter(ticket_type=1).order_by('-start_time')
  if len(token_record) > 0:
    token_record = token_record[0]
  else:
    token_record = Ticket()
  token_record.content = token
  token_record.end_time = endtime
  token_record.save()
  return token_record

def update_jsapi():
  print 'update jsapi'
  params = {
    'access_token': get_ticket(1).content,
    'type': 'jsapi',
  }
  host = 'api.weixin.qq.com'
  path = '/cgi-bin/ticket/getticket'
  method = 'GET'
 
  res = send_request(host, path, method, params=params)
  if not res[0]:
    return False
  if res[1].get('errcode'):
    return False
  token = res[1].get('ticket')
  starttime = timezone.now()
  expires_in = timedelta(seconds=int(res[1].get('expires_in')))
  endtime = starttime + expires_in
  token_record = Ticket.objects.filter(ticket_type=2).order_by('-start_time')
  if len(token_record) > 0:
    token_record = token_record[0]
  else:
    token_record = Ticket()
  token_record.content = token
  token_record.end_time = endtime
  token_record.ticket_type = 2
  token_record.save()
  return token_record