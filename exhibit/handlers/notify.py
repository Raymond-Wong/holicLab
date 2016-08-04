# -*- coding: utf-8 -*-
import sys
sys.path.append('..')
reload(sys)
sys.setdefaultencoding('utf-8')
import json
from datetime import timedelta
try: 
  import xml.etree.cElementTree as ET
except ImportError: 
  import xml.etree.ElementTree as ET

from django.http import HttpResponse, HttpRequest, HttpResponseServerError, Http404
from django.utils.encoding import smart_str

from holicLab.utils import *
from holicLab.models import Order, Shop, User, Course, Bookable_Time

def notify(request):
  # 待返回信息
  RET_STR = '<xml><return_code><![CDATA[%s]]></return_code><return_msg><![CDATA[%s]]></return_msg></xml>'
  print request.body
  return HttpResponse(RET_STR % ('SUCCESS', 'OK'))