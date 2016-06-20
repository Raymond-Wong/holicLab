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
      return HttpResponse(Response(c=-1, m=e, s='failed').toJson(), content_type='application/json')
  return unKnownErr

def login_required(view):
  def verified(request, *args, **kwargs):
    try:
      request.session['uid']
      return view(request, *args, **kwargs)
    except:
      return redirect('/login')
  return verified
