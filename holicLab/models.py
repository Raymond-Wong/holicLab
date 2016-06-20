# -*- coding: utf-8 -*-
from django.db import models

# 用户类
# 微信openid，昵称，电话号码，总预约次数，总预约天数，总预约时长
USER_ROLES = ((1, u'admin'), (2, 'member'))
class User(models.Model):
  wx_openid = models.TextField(blank=False)
  nickname = models.CharField(max_length=100, blank=False)
  phone = models.CharField(max_length=20, default='')
  role = models.CharField(max_length=2, choices=USER_ROLES, default=2)
  total_order_times = models.PositiveIntegerField(default=0)
  total_order_days = models.PositiveIntegerField(default=0)
  total_order_duration = models.PositiveIntegerField(default=0)

  def __unicode__(self):
    return self.nickname

# 优惠券抽象类
# 名称，减免价格，描述，所属的用户
class Coupon(models.Model):
  name = models.CharField(max_length=20, blank=False)
  price = models.PositiveIntegerField(blank=False)
  description = models.CharField(max_length=100)
  user = models.ForeignKey(User)
  def __unicode__(self):
    return self.name
# 时限类优惠券
class Time_Limit_Coupon(Coupon):
  start_time = models.DateTimeField()
  end_time = models.DateTimeField()
# 次数限制类优惠券
class Tries_Limit_Coupon(Coupon):
  reuse_times = models.IntegerField(default=-1)

# 服务类
class Service(models.Model):
  name = models.CharField(max_length=20)
  price = models.PositiveIntegerField(blank=False)
  description = models.CharField(max_length=100)

# 门店类
class Shop(models.Model):
  name = models.CharField(max_length=50)
  location = models.CharField(max_length=200)
  price = models.PositiveIntegerField(default=0)
  capacity = models.PositiveIntegerField(default=0)

# 时间段类，记录每个时间段已预约的人数
class Time_Bucket(models.Model):
  date = models.DateField()
  occupation = models.TextField()

# 课程状态枚举
COURSE_STATE = ((1, u'unstarted'), (2, u'started'), (3, u'full'), (4, u'time_out'), (5, u'finished'))
# 课程类
class Course(models.Model):
  name = models.CharField(max_length=50)
  description = models.TextField()
  start_time = models.DateTimeField()
  end_time = models.DateTimeField()
  tags = models.TextField()
  price = models.PositiveIntegerField()
  state = models.CharField(max_length=20, choices=COURSE_STATE, default='started')
  capacity = models.PositiveIntegerField(default=0)
  sign_up_ddl = models.DateTimeField()
  shop = models.ForeignKey(Shop)

# 服务类
class Service(models.Model):
  name = models.CharField(max_length=20)
  description = models.CharField(max_length=100)
  price = models.PositiveIntegerField(default=0)
  shop = models.ForeignKey(Shop)

# 密码类
class Password(models.Model):
  start_time = models.DateTimeField()
  end_time = models.DateTimeField()
  used_times = models.PositiveIntegerField(default=0)
  content = models.CharField(max_length=4)

# 订单类型枚举
ORDER_TYPE = ((1, u'site'), (2, u'course'))
# 订单状态枚举
ORDER_STATE = ((1, u'to_pay'), (2, u'cancel'), (3, u'time_out'), (4, u'success'))
# 订单类
class Order(models.Model):
  create_time = models.DateTimeField(auto_now_add=True)
  pay_time = models.DateTimeField()
  finish_time = models.DateTimeField()
  user = models.OneToOneField(User)
  price = models.PositiveIntegerField()
  course = models.ForeignKey(Course)
  order_type = models.CharField(max_length=10, choices=ORDER_TYPE)
  coupons = models.ForeignKey(Coupon)
  password = models.OneToOneField(Password)
  start_time = models.DateTimeField()
  end_time = models.DateTimeField()
  people_amount = models.PositiveIntegerField(default=1)
  services = models.ManyToManyField(Service)
  state = models.CharField(max_length=20, choices=ORDER_STATE)
  shop = models.ForeignKey(Shop)
  def __unicode__(self):
    return '%s->%s' % (self.user.id, self.create_time)