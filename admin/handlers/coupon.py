# -*- coding: utf-8 -*-
import sys
sys.path.append('..')
reload(sys)
sys.setdefaultencoding('utf-8')
import json
import time
import datetime

from django.http import HttpResponse, HttpRequest, HttpResponseServerError, Http404
from django.shortcuts import render_to_response, redirect
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers

from holicLab.utils import *
from holicLab.models import User

def list(request):
  if request.method == 'GET':
    members = User.objects.all()
    return render_to_response('admin/coupon.html', {'members' : members, 'activePage' : 'coupon'})