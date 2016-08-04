# -*- coding: utf-8 -*-
import sys
sys.path.append('..')
reload(sys)
sys.setdefaultencoding('utf-8')
import json
import httplib
import urllib, urllib2
import random
import re
from datetime import datetime, date
from django.db import models
try: 
  import xml.etree.cElementTree as ET
except ImportError: 
  import xml.etree.ElementTree as ET

from django.http import HttpResponse, HttpRequest, HttpResponseServerError, Http404

class Response:
  def __init__(self, c=0, m=""):
    self.code = c
    self.msg = m
  def toJson(self):
    tmp = {}
    tmp["code"] = self.code
    tmp["msg"] = self.msg
    return json.dumps(tmp, ensure_ascii=False)

def md5(str):
  import hashlib
  m = hashlib.md5()
  m.update(str.encode("utf8"))
  return m.hexdigest()

def sha1(string):
  import hashlib
  return hashlib.sha1(string).hexdigest()

class MyJsonEncoder(json.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, datetime):
      return obj.strftime('%Y-%m-%d %H:%M:%S')
    elif isinstance(obj, date):
      return obj.strftime('%Y-%m-%d')
    elif isinstance(obj, models.Model):
      return None
    else:
      return json.JSONEncoder.default(self, obj)

# 获得图片的完整链接
def appendImageUrl(x):
  from os import environ
  remote = environ.get("APP_NAME", "")
  remote_media_path = "http://holicLab-images.stor.sinaapp.com/"
  IMAGE_BASE_URL = remote_media_path if remote else "/media/"
  if type(x) == dict:
    x["image"] = IMAGE_BASE_URL + x.get("image", "")
  elif type(x) == str or type(x) == unicode:
    x = IMAGE_BASE_URL + x
  else:
    x = "/static/pc/icon/logo.png"
  return x

# 发送请求
# 如果发送请求时服务器返回的是access_token过期的话，就跑出一个PastDueException
def send_request(host, path, method, port=443, params={}, toLoad=True):
  client = httplib.HTTPSConnection(host, port)
  if method == 'GET':
    path = '?'.join([path, urllib.urlencode(params)])
    client.request(method, path)
  else:
    client.request(method, path, json.dumps(params, ensure_ascii=False).encode('utf8'))
    # client.request(method, path, urllib.urlencode(params))
  res = client.getresponse()
  if not res.status == 200:
    return False, res.status
  resStr = res.read()
  if toLoad:
    resDict = json.loads(resStr, encoding="utf-8")
    if 'errcode' in resDict.keys() and resDict['errcode'] == 40001:
      raise PastDueException('access token past due')
    if 'errcode' in resDict.keys() and resDict['errcode'] != 0:
      return False, resDict
    return True, resDict
  else:
    return True, resStr

def send_xml(url, data):
  # cookies = urllib2.HTTPCookieProcessor()
  # opener = urllib2.build_opener(cookies)
  # request = urllib2.Request(url=url, headers={'Content-Type' : 'application/xml','charset':'UTF-8'}, data=data)
  # f = opener.open(request)
  # return f.read()
  return urllib2.urlopen(url, data, timeout=30).read()

CODE_RANGE = [str(i) for i in xrange(0, 10)] + [chr(i) for i in xrange(97, 123)] + [chr(i) for i in xrange(65, 91)]
# 随机生成一个x位的码
def random_x_bit_code(x, code_range=CODE_RANGE):
  ret = ''
  for i in xrange(x):
    ret += random.choice(code_range)
  return ret

# def sendSMS(mobile, code):
#   #服务地址
#   sms_host = "api.dingdongcloud.com"
#   #端口号
#   port = 443
#   #发送验证码
#   send_yzm_uri = "/v1/sms/sendyzm"
#   #修改为您的apikey. apikey可在官网（https://www.dingdongcloud.com)登录后获取
#   apikey = "149befbfbe656696c2d904057afa8fd6"; 
#   # 修改为您要发送的短信内容
#   content="【好叻健身试炼仓】尊敬的用户，你的验证码是：%s，请在10分钟内输入。请勿告诉其他人。" % code
#   """
#   发送验证码
#   """
#   params = urllib.urlencode({'apikey': apikey, 'content': content, 'mobile':mobile})
#   headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
#   conn = httplib.HTTPSConnection(sms_host, port=port, timeout=30)
#   conn.request("POST", send_yzm_uri, params, headers)
#   response = conn.getresponse()
#   response_str = response.read()
#   conn.close()
#   return response_str

def sendSMS(mobile, code):
  print code
  params = {}
  params['code'] = 0
  return json.dumps(params)

def filterEmoji(desstr,restr=''):
  try:
    co = re.compile(u'[\U00010000-\U0010ffff]')
  except re.error:
    co = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
  return co.sub(restr, desstr)

def getUserIp(request):
  if request.META.has_key('HTTP_X_FORWARDED_FOR'):
    ip =  request.META['HTTP_X_FORWARDED_FOR'].split(',')[0]
  else:  
    ip = request.META['REMOTE_ADDR'] 
  return ip

# 将字典解析成xml
def dict2xml(root, d):
  if isinstance(d, dict):
    for key in sorted(d.keys()):
      child = ET.SubElement(root, key)
      child = dict2xml(child, d[key])
  elif isinstance(d, list):
    for item in sorted(d):
      for key in item.keys():
        child = ET.SubElement(root, key)
        child = dict2xml(child, item[key])
  else:
    if isinstance(d, int) or isinstance(d, float):
      d = str(d)
    root.text = d
  return root
