# -*- coding: utf-8 -*-
import sys

from django.http import HttpResponse
from django.shortcuts import redirect
from utils import Response

def handler(view):
  def unKnownErr(request, *args, **kwargs):
    try:
      return view(request, *args, **kwargs)
    except Exception, e:
      return HttpResponse(Response(c=-1, m=e).toJson(), content_type='application/json')
  return unKnownErr

def login_required(view):
  def verified(request, *args, **kwargs):
    try:
      if request.session['logined']:
        return view(request, *args, **kwargs)
    except:
      return redirect('/admin/login')
  return verified
