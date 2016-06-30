# -*- coding: utf-8 -*-
import sys
sys.path.append('..')
reload(sys)
sys.setdefaultencoding('utf-8')
import json
from datetime import datetime, date
from django.db import models

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
  m.update(str)
  return m.hexdigest()

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
  print 'appendImageUrl'
  from django.conf import settings
  remote_media_path = "http://holicLab-images.stor.sinaapp.com/"
  IMAGE_BASE_URL = remote_media_path if settings.REMOTE else "/media/"
  print settings.REMOTE
  print IMAGE_BASE_URL
  if type(x) == dict:
    x["image"] = IMAGE_BASE_URL + x.get("image", "")
  elif type(x) == str or type(x) == unicode:
    x = IMAGE_BASE_URL + x
  else:
    x = "/static/pc/icon/logo.png"
  return x