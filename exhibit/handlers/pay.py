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
from django.db.models import F

import holicLab.settings as settings
from holicLab.utils import *
from holicLab.models import Order, Shop, User, Course, Bookable_Time, Time_Bucket

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
  newOrder, tmpCoupon = getOrderPrice(newOrder, (newOrder.end_time - newOrder.start_time).seconds / 60)
  # 获取prepayid
  prepay_id = getPrePayId(newOrder, request)
  if not prepay_id[0]:
    return HttpResponse(Response(c=1, m=prepay_id[1]).toJson(), content_type="application/json")
  # 获取前段需要的签名
  params = {}
  params['appId'] = settings.WX_APP_ID
  params['timeStamp'] = str(int(time.time()))
  params['nonceStr'] = random_x_bit_code(10)
  params['package'] = 'prepay_id=%s' % prepay_id[1]
  params['signType'] = 'MD5'
  toSignStr = '&'.join(map(lambda x:x[0] + '=' + x[1], sorted(params.iteritems(), lambda x,y:cmp(x[0], y[0]))))
  toSignStr += ('&key=' + settings.WX_MCH_KEY)
  params['paySign'] = md5(toSignStr).upper()
  params['oid'] = newOrder.oid
  newOrder.save()
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
  newOrder, tmpCoupon = getOrderPrice(newOrder, (newOrder.end_time - newOrder.start_time).seconds / 60)
  return HttpResponse(Response(m=(newOrder.price / 10.0)).toJson(), content_type="application/json")

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
    if to_book_time.occupation + i <= course.capacity:
      params['bookable_amount'].append(i);
  if to_book_time.occupation == 0:
    params['bookable_amount'].append('包场')
  return render(request, 'exhibit/order_pre.html', params)

def check(request):
  order = Order.objects.get(oid=request.POST.get('oid'))
  if order.state != "1":
    return HttpResponse(Response(m={'status' : 'SUCCESS', 'desc' : '订单处理完毕', 'url' : '/order?action=success&oid=%s' % order.oid}).toJson(), content_type="application/json")
  user = User.objects.get(invite_code=request.session['user'])
  params = {}
  params['appid'] = settings.WX_APP_ID
  params['mch_id'] = settings.WX_MCH_ID
  params['nonce_str'] = random_x_bit_code(20)
  params['out_trade_no'] = str(order.oid)
  toSignStr = '&'.join(map(lambda x:x[0] + '=' + x[1], sorted(params.iteritems(), lambda x,y:cmp(x[0], y[0]))))
  toSignStr += ('&key=' + settings.WX_MCH_KEY)
  # 在xml最后面加入签名
  xml = dict2xml(ET.Element('xml'), params)
  signNode = ET.SubElement(xml, 'sign')
  signNode.text = md5(toSignStr).upper()
  msg = ET.tostring(xml, 'utf-8')
  res = send_xml('https://api.mch.weixin.qq.com/pay/orderquery', msg)
  res = ET.fromstring(smart_str(res))
  res = xml2dict(res)
  if res['return_code'] != 'SUCCESS':
    return HttpResponse(Response(m={'status' : 'RETRY', 'desc' : '请耐心等候...', 'url' : ''}).toJson(), content_type="application/json")
  # 如果订单状态为支付成功，则修改订单状态
  if res['trade_state'] == 'USERPAYING':
    # 如果订单状态为用户支付中，则要求重新检查用户支付状态
    return HttpResponse(Response(m={'status' : 'RETRY', 'desc' : '请耐心等候...', 'url' : ''}).toJson(), content_type="application/json")
  elif res['trade_state'] == 'SUCCESS':
    successOrder(order, res['trade_state'], res['time_end'])
    return HttpResponse(Response(m={'status' : 'SUCCESS', 'desc' : '订单处理完毕', 'url' : '/order?action=success&oid=%s' % order.oid}).toJson(), content_type="application/json")
  else:
    order.state = "3"
    order.save()
  successOrder(order, res['trade_state'])
  # 如果订单状态为失败，则告知失败
  return HttpResponse(Response(m={'status' : 'FAILED', 'desc' : '请联系工作人员', 'url' : ''}).toJson(), content_type="application/json")

def cancel(request):
  order = Order.objects.get(oid=request.POST.get('oid'))
  order.delete()
  return HttpResponse(Response(m='取消订单成功').toJson(), content_type="application/json")

# 传入一个order对象，获取其价格
def getOrderPrice(newOrder, duration):
  # 计算基础价格
  newOrder.price = 0
  if int(newOrder.order_type) == 1:
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
  # 计算当前下单时间离商店发布时间的差
  user = newOrder.user
  # 使用的优惠券数量
  usedCoupon = 0
  sinceShopRelease = timezone.now().date() - newOrder.shop.releaseDate
  if sinceShopRelease.days / 30.0 <= 1:
    # 如果当前订单离商店发布时间在一个月内
    if str(user.user_type) == "1":
      newOrder.price = newOrder.price / 2
      # 如果用户是被邀请的，则每一小时可以减免十元
      if user.invited_by != None:
        newOrder.price, usedCoupon = getCouponPrice(newOrder.price, user.balance, duration)
  elif sinceShopRelease.days / 30.0 <= 2:
    # 如果当前订单离商店发布时间在两个月内
    if str(user.user_type) == "1":
      newOrder.price = newOrder.price / 2
  else:
    # 如果当前订单离商店发布时间三个月以上，则只能根据balance进行减免
    newOrder.price, usedCoupon = getCouponPrice(newOrder.price, user.balance, duration)
  # 如果优惠后的价格小于0，则为0
  newOrder.price = 0 if newOrder.price < 0  else newOrder.price
  return newOrder, usedCoupon

def getCouponPrice(price, balance, duration):
  coupon = duration / 60
  coupon = coupon if balance > coupon else balance
  price = price - 100 * coupon
  return price, coupon

def getPrePayId(order, request):
  user = User.objects.get(invite_code=request.session['user'])
  params = {}
  params['openid'] = user.wx_openid
  params['device_info'] = 'WEB'
  params['appid'] = settings.WX_APP_ID
  params['mch_id'] = settings.WX_MCH_ID
  params['nonce_str'] = random_x_bit_code(20)
  params['body'] = 'HolicLab - %s预约' % ('场地' if order.order_type == 1 else '课程')
  params['out_trade_no'] = str(order.oid)
  # params['total_fee'] = str(int(order.price * 10))
  params['total_fee'] = "1"
  params['spbill_create_ip'] = str(getUserIp(request))
  params['notify_url'] = 'http://holicLab.applinzi.com/order/notify'
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
  if res['return_code'] == 'SUCCESS' and res['return_msg'] == 'OK':
    return True, res['prepay_id']
  return False, '发起支付请求失败，请联系客服人员'

# 订单支付成功后修改数据
def successOrder(order, status, time_end):
  # 1. 修改订单的状态
  if status == 'SUCCESS':
    order.state = "4"
    order.pay_time = datetime.strptime(time_end, '%Y%m%d%H%M%S')
  else:
    order.delete()
    return None
  user = order.user
  # 2. 如果该用户是新用户且是被邀请用户的话，邀请他的用户可以获得优惠券
  if user.invited_by and user.user_type == "1":
    invite_user = user.invited_by
    invite_user.balance = F('balance') + 1
    invite_user.save()
  # 3. 设置该用户为老用户
  user.user_type = "2"
  # 2.1 更新该用户的优惠券数量
  priceBK = order.price
  price, usedCoupon = getOrderPrice(order, (order.end_time - order.start_time).seconds / 60)
  order.price = priceBK
  user.balance = F('balance') - usedCoupon
  user.balance = F('balance') if F('balance') >= 0 else 0
  # 2.2 更新用户消费总金额
  user.consumption = F('consumption') + order.price
  # 4. 修改订单涉及课程或者场地的占用人次
  if order.order_type == "1":
    shop = order.shop
    duration = int((order.end_time - order.start_time).total_seconds()) / 60
    for period in xrange(duration / 30):
      start_time = order.start_time + timedelta(seconds=60*30*period)
      timeBucket = None
      try:
        timeBucket = Time_Bucket.objects.filter(shop=shop).get(start_time=start_time)
      except:
        timeBucket = Time_Bucket()
        timeBucket.start_time = start_time
        timeBucket.shop = order.shop
        timeBucket.occupation = 0
        timeBucket.save()
      timeBucket.occupation = F('occupation') + 1
      timeBucket.save()
  else:
    course = order.course
    bookableTime = Bookable_Time.objects.filter(course=course).get(start_time=order.start_time)
    bookableTime.occupation = F('occupation') + 1
    bookableTime.save()
  # 保存对象
  order.save()
  user.save()
