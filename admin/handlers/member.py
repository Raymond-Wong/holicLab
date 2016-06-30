# -*- coding: utf-8 -*-
import sys
sys.path.append('..')
reload(sys)
sys.setdefaultencoding('utf-8')
import json
import time
import datetime

from django.http import HttpResponse, HttpRequest, HttpResponseServerError, Http404
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers

from holicLab.utils import *
from holicLab.models import User

def list(request):
  if request.method == 'GET':
    user_type = request.GET.get('state', 'old')
    members = User.objects.filter(user_type=(1 if user_type == 'new' else 2))
    return render(request, 'admin/member.html', {'members' : members, 'activePage' : 'member'})
  # 检查数据合法性
  times_lb = request.POST.get('times_lb', 0)
  times_ub = request.POST.get('times_ub', str(sys.maxint))
  days_lb = request.POST.get('days_lb', 0)
  days_ub = request.POST.get('days_ub', str(sys.maxint))
  duration_lb = request.POST.get('duration_lb', 0)
  duration_ub = request.POST.get('duration_ub', str(sys.maxint))
  try:
    times_lb = int(times_lb)
    times_ub = int(times_ub)
    days_lb = int(days_lb)
    days_ub = int(days_ub)
    duration_lb = int(duration_lb)
    duration_ub = int(duration_ub)
  except:
    return HttpResponse(Response(c=2, m='上下限必须为数值'))
  if times_lb > times_ub or days_lb > days_ub or duration_lb > duration_ub:
    return HttpResponse(Response(c=1, m='下限必须小于上限'))
  members = Member.objects.filter(total_order_times__gte=times_lb).filter(total_order_times__lt=times_ub)
  members = members.filter(total_order_days__gte=days_lb).filter(total_order_days__lt=days_ub)
  members = members.filter(total_order_duration__gte=duration_lb).filter(total_order_duration__lt=duration_ub)
  return HttpResponse(Response(m=serializers.serialize("json", members)).toJson(), content_type='application/json')
