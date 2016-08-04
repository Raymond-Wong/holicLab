# -*- coding: utf-8 -*-
import sys
sys.path.append('..')
reload(sys)
sys.setdefaultencoding('utf-8')
import json
import time
import qrcode
import base64
import cStringIO
from datetime import timedelta
try: 
  import xml.etree.cElementTree as ET
except ImportError: 
  import xml.etree.ElementTree as ET

from django.http import HttpResponse, HttpRequest, HttpResponseServerError, Http404
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.utils import timezone
from django.utils.encoding import smart_str

import holicLab.settings as settings
from holicLab.utils import *
from holicLab.models import Order, Shop, User, Course, Bookable_Time

def add(request):
  user = User.objects.get(invite_code=request.session['user'])
  newOrder = Order()
  newOrder.order_type = int(request.POST.get('type', None))
  newOrder.user = user
  newOrder.oid = user.invite_code + str(int(time.time() * 1000))
  newOrder.people_amount = int(request.POST.get('amount', None))
  newOrder.services = request.POST.get('services', "[]")
  if newOrder.order_type == 1:
    newOrder.shop = Shop.objects.get(id=request.POST.get('sid'))
    newOrder.start_time = datetime.strptime(request.POST.get('start_time', None), '%a, %d %b %Y, %H:%M')
    newOrder.end_time = newOrder.start_time + timedelta(minutes=int(request.POST.get('duration', None)))
  else:
    newOrder.course = Course.objects.get(id=request.POST.get('cid'))
    newOrder.shop = newOrder.course.shop
    bookable_time = Bookable_Time.objects.get(id=request.POST.get('bid', None))
    newOrder.start_time = bookable_time.start_time
    newOrder.end_time = bookable_time.end_time
  newOrder = getOrderPrice(newOrder, (newOrder.end_time - newOrder.start_time).seconds / 60)
  # 获取prepayid
  prepay_id = getPrePayId(newOrder, request)
  if not prepay_id[0]:
    return HttpResponse(Response(c=1, m=prepay_id[1]).toJson(), content_type="application/json")
  # 获取前段需要的签名
  params = {}
  params['appId'] = settings.WX_APP_ID
  params['timeStamp'] = str(int(time.time()))
  params['nonceStr'] = random_x_bit_code(10)
  params['package'] = prepay_id[1]
  params['signType'] = 'MD5'
  toSignStr = '&'.join(map(lambda x:x[0] + '=' + x[1], sorted(params.iteritems(), lambda x,y:cmp(x[0], y[0]))))
  params['paySign'] = md5(toSignStr).upper()
  # newOrder.save()
  return HttpResponse(Response(m=params).toJson(), content_type="application/json")

def price(request):
  user = User.objects.get(invite_code=request.session['user'])
  newOrder = Order()
  newOrder.order_type = int(request.POST.get('type', None))
  newOrder.user = user
  newOrder.people_amount = int(request.POST.get('amount', None))
  newOrder.services = request.POST.get('services', "[]")
  if newOrder.order_type == 1:
    newOrder.shop = Shop.objects.get(id=request.POST.get('sid'))
    newOrder.start_time = datetime.strptime(request.POST.get('start_time', None), '%a, %d %b %Y, %H:%M')
    newOrder.end_time = newOrder.start_time + timedelta(minutes=int(request.POST.get('duration', None)))
  else:
    newOrder.course = Course.objects.get(id=request.POST.get('cid'))
    newOrder.shop = newOrder.course.shop
    bookable_time = Bookable_Time.objects.get(id=request.POST.get('bid', None))
    newOrder.start_time = bookable_time.start_time
    newOrder.end_time = bookable_time.end_time
  newOrder = getOrderPrice(newOrder, (newOrder.end_time - newOrder.start_time).seconds / 60)
  return HttpResponse(Response(m=newOrder.price).toJson(), content_type="application/json")

def pre(request):
  order_type = request.GET.get('type', None)
  if order_type == 'site':
    return pre_site_order(request)
  elif order_type == 'course':
    return pre_course_order(request)
  return HttpResponse(Response(c=1, m="待添加订单类型错误").toJson(), content_type="application/json")

def pre_site_order(request):
  # 判断数据合法性
  sid = request.GET.get('sid', None)
  shop = None
  timestamp = request.GET.get('timestamp', None)
  try:
    shop = Shop.objects.get(id=int(sid))
  except Exception:
    return HttpResponse(Response(c=2, m='待预定场地不存在').toJson(), content_type='application/json')
  start_time = datetime.fromtimestamp(float(timestamp))
  now = datetime.now()
  if start_time < now:
    return HttpResponse(Response(c=3, m='待预约时间已过期').toJson(), content_type='application/json')
  params = {}
  user = User.objects.get(invite_code=request.session['user'])
  params['is_first_order'] = True if len(user.order_set.filter(state=4)) == 0 else False
  params['balance'] = user.balance
  params['cover'] = json.loads(shop.cover)[0]
  params['title'] = shop.name
  params['startTime'] = start_time.strftime('%a, %d %b %Y, %H:%M')
  params['location'] = shop.location
  params['type'] = 'site'
  params['price'] = shop.price
  params['capacity'] = shop.capacity
  params['id'] = shop.id
  params['bookable_time'] = []
  current_time = start_time
  for i in xrange(1, 4):
    current_time = current_time + timedelta(minutes=i * 30)
    params['bookable_time'].append({'duration' : (i + 1) * 30, 'bookable' : True if getTimeOccupation(shop, current_time) < shop.capacity else False})
  params['bookable_amount'] = []
  start_time_occupation = getTimeOccupation(shop, start_time)
  for i in xrange(1, 4):
    if start_time_occupation + i < shop.capacity:
      params['bookable_amount'].append(i)
  if start_time_occupation == 0:
    params['bookable_amount'].append('包场')
  return render(request, 'exhibit/order_pre.html', params)

def getTimeOccupation(shop, time):
  time_bucket = shop.time_bucket_set.filter(start_time=time)
  ret = 0
  if len(time_bucket):
    ret = time_bucket[0].occupation
  return ret

def pre_course_order(request):
    # 判断数据合法性
  cid = request.GET.get('cid', None)
  bid = request.GET.get('bid', None)
  course = None
  to_book_time = None
  try:
    course = Course.objects.get(id=int(cid))
  except Exception:
    return HttpResponse(Response(c=2, m='待预定课程不存在').toJson(), content_type='application/json')
  try:
    to_book_time = Bookable_Time.objects.get(id=int(bid))
  except Exception, e:
    return HttpResponse(Response(c=3, m='待预定课程在待预定时间内没开课').toJson(), content_type='application/json')
  now = timezone.now()
  if to_book_time.start_time < now:
    return HttpResponse(Response(c=4, m='待预约时间已过期').toJson(), content_type='application/json')
  params = {}
  user = User.objects.get(invite_code=request.session['user'])
  params['is_first_order'] = True if len(user.order_set.filter(state=4)) == 0 else False
  params['balance'] = user.balance
  params['cover'] = json.loads(course.cover)[0]
  params['title'] = course.name
  params['type'] = 'course'
  params['startTime'] = timezone.localtime(to_book_time.start_time).strftime('%a, %d %b %Y, %H:%M') + '-' + timezone.localtime(to_book_time.end_time).strftime('%H:%M')
  params['bid'] = bid
  params['location'] = course.shop.location
  params['price'] = course.price
  params['capacity'] = course.capacity
  params['id'] = course.id
  params['bookable_amount'] = []
  for i in xrange(1, 4):
    if to_book_time.occupation + i < course.capacity:
      params['bookable_amount'].append(i);
  if to_book_time.occupation == 0:
    params['bookable_amount'].append('包场')
  return render(request, 'exhibit/order_pre.html', params)

def list(request):
  invite_code = request.session['user']
  orderType = request.GET.get('type', '0')
  user = None
  try:
    user = User.objects.get(invite_code=invite_code)
  except:
    return HttpResponse(Response(c=-2, m="待查询用户不存在").toJson(), content_type="application/json")
  if orderType == "1" or orderType == "2":
    orders = user.order_set.filter(order_type=orderType)
  else:
    orders = user.order_set.all()
    orderType = "0"
  # 处理duration
  for order in orders:
    order.price = int(order.price / 10.0)
    if order.order_type == "1":
      order.duration = order.end_time - order.start_time
      order.duration = order.duration.seconds / 60.0
      order.duration = str(int(order.duration)) + 'min'
      print order.duration
  return render(request, 'exhibit/order_list.html', {'orders' : orders, 'type' : orderType})

def get(request):
  oid = request.GET.get('oid', None)
  if oid is None:
    return HttpResponse(Response(c=-9, m="未提供待查询订单id").toJson(), content_type="application/json")
  order = None
  try:
    order = Order.objects.get(id=oid)
  except:
    return HttpResponse(Response(c=-5, m="待查询订单不存在").toJson(), content_type="application/json")
  if order.order_type == "1":
    order.cover = json.loads(order.shop.cover)[0]
  else:
    order.cover = json.loads(order.course.cover)[0]
  order.services = json.loads(order.services)
  if 'food' in order.services:
    order.food = True
  if 'coach' in order.services:
    order.coach = True
  order.price /= 10.0
  return render(request, 'exhibit/order_get.html', {'order' : order})

def update(request):
  oid = request.GET.get('oid', None)
  if oid is None:
    return HttpResponse(Response(c=-9, m="未提供待查询订单id").toJson(), content_type="application/json")
  order = None
  try:
    order = Order.objects.get(id=oid)
  except:
    return HttpResponse(Response(c=-5, m="待查询订单不存在").toJson(), content_type="application/json")
  order.state = 4
  order.save()
  return HttpResponse(Response(m="订单状态更新成功").toJson(), content_type="application/json")

# 传入一个order对象，获取其价格
def getOrderPrice(newOrder, duration):
  # 计算基础价格
  newOrder.price = 0
  if newOrder.order_type == 1:
    newOrder.price = newOrder.shop.price
    newOrder.price = duration / 30 * newOrder.price
  else:
    newOrder.price = newOrder.course.price
  newOrder.price = float(newOrder.price)
  for service in json.loads(newOrder.services):
    if service == 'food':
      newOrder.price += 500
    elif service == 'coach':
      newOrder.price += 1000
  newOrder.price = newOrder.people_amount * newOrder.price
  # 计算优惠
  user = newOrder.user
  if len(user.order_set.filter(state=4)) == 0:
    newOrder.price = newOrder.price / 2
  else:
    coupon = duration / 60
    coupon = coupon if user.balance > coupon else user.balance
    newOrder.price = newOrder.price - 100 * coupon
  return newOrder

def password(request):
  if request.method == 'POST':
    user = User.objects.get(invite_code=request.session['user'])
    now = timezone.now()
    now = timedelta(minutes=15)
    order = user.order_set.filter(start_time__lte=now).filter(end_time__gt=now)
    if len(order) == 0:
      return HttpResponse(Response(c=1, m='获取密码失败，请在预约时间前15分钟点击获取密码'))
    order = order[0]
    return HttpResponse(Response(m='/order?action=password&oid=%s') % str(order.id).toJson(), content_type="application/json")
  url = 'http://holicLab.applinzi.com/order?action=get&oid=' + request.GET.get('oid')
  img = qrcode.make(url)
  img_buffer = cStringIO.StringIO()
  img.save(img_buffer, format='PNG')
  qrcode = 'data:image/png;base64,' + base64.b64encode(img_buffer.getvalue())
  return render(request, 'exhibit/order_password.html', {'order' : order, 'qrcode' : qrcode})

def getPrePayId(order, request):
  user = User.objects.get(invite_code=request.session['user'])
  params = {}
  params['openid'] = user.wx_openid
  params['device_info'] = 'WEB'
  params['appid'] = settings.WX_APP_ID
  params['mch_id'] = settings.WX_MCH_ID
  params['nonce_str'] = random_x_bit_code(20)
  params['body'] = 'HolicLab-site/course booking'
  params['out_trade_no'] = str(order.oid)
  params['total_fee'] = str(int(order.price * 10))
  params['spbill_create_ip'] = str(getUserIp(request))
  params['notify_url'] = 'http://holicLab.applinzi.com/notify'
  params['trade_type'] = 'JSAPI'
  toSignStr = '&'.join(map(lambda x:x[0] + '=' + x[1], sorted(params.iteritems(), lambda x,y:cmp(x[0], y[0]))))
  toSignStr += ('&key=' + settings.WX_MCH_KEY)
  # 在xml最后面加入签名
  xml = dict2xml(ET.Element('xml'), params)
  signNode = ET.SubElement(xml, 'sign')
  signNode.text = md5(toSignStr).upper()
  msg = ET.tostring(xml, 'utf-8')
  res = send_xml('https://api.mch.weixin.qq.com/pay/unifiedorder', msg)
  res = ET.fromstring(smart_str(res))
  res = xml2dict(res)
  print 'res:', res
  print 'return_msg:', res['return_msg']
  if res['return_code'] == 'SUCCESS' and res['return_msg'] == 'OK':
    return True, res['prepay_id']
  return False, '发起支付请求失败，请联系客服人员'




