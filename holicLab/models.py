# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import ImageField
from django.db.models.fields.files import ImageFieldFile, FieldFile, ImageFile
import sae.storage
from os import environ

# 用户类
# 微信openid，昵称，电话号码，总预约次数，总预约天数，总预约时长
USER_TYPE = ((1, u'new'), (2, u'old'))
GENDER = ((u'f', u'female'), (u'm', u'male'))
USER_ROLE = ((1, u'student'), (2, u'staff'))
class User(models.Model):
  wx_openid = models.TextField(blank=True)
  nickname = models.CharField(max_length=100, blank=False)
  phone = models.CharField(max_length=11, default='')
  bind_date = models.DateField(null=True)
  gender = models.CharField(max_length=6, choices=GENDER, default='m')
  role = models.CharField(max_length=7, choices=USER_ROLE, default=1)
  total_order_times = models.PositiveIntegerField(default=0)
  total_order_days = models.PositiveIntegerField(default=0)
  total_order_duration = models.PositiveIntegerField(default=0)
  invite_code = models.CharField(max_length=6, unique=True)
  invited_by = models.ForeignKey('self', null=True)
  balance = models.PositiveIntegerField(default=0)
  consumption = models.PositiveIntegerField(default=0)
  user_type = models.CharField(max_length=3, choices=USER_TYPE, default=1)

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

# 封面类型
COVER_TYPE = ((1, u'image'), (2, u'video'))
SHOP_STATE = ((1, u'unreleased'), (2, u'released'))
# 门店类
class Shop(models.Model):
  name = models.CharField(max_length=50)
  description = models.TextField()
  notice = models.TextField()
  cover_type = models.CharField(max_length=5, choices=COVER_TYPE, default=1)
  cover = models.TextField()
  location = models.CharField(max_length=200)
  price = models.PositiveIntegerField(default=0)
  capacity = models.PositiveIntegerField(default=0)
  invalide_times = models.TextField()
  last_modified_time = models.DateTimeField(auto_now=True)
  state = models.CharField(max_length=10, choices=SHOP_STATE, default=1)
  password = models.CharField(max_length=6, blank=True)
  phone = models.CharField(max_length=11, default='')
  def toJSON(self):
    import json
    import utils
    return json.dumps(dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]]), ensure_ascii=False, cls=utils.MyJsonEncoder)

# 课程状态枚举
COURSE_STATE = ((1, u'started'), (2, u'full'), (3, u'time_out'), (4, u'finished'))
# 课程类
class Course(models.Model):
  name = models.CharField(max_length=50)
  description = models.TextField()
  coach_description = models.TextField()
  coach_cover = models.TextField()
  cover_type = models.CharField(max_length=5, choices=COVER_TYPE, default=1)
  cover = models.TextField()
  price = models.PositiveIntegerField()
  course_state = models.CharField(max_length=20, choices=COURSE_STATE, default='started')
  tags = models.TextField(blank=True)
  capacity = models.PositiveIntegerField(default=0)
  shop = models.ForeignKey(Shop)
  last_modified_time = models.DateTimeField(auto_now=True)
  state = models.CharField(max_length=10, choices=SHOP_STATE, default=1)
  notice = models.TextField()
  duration = models.CharField(max_length=50, default=u'一小时')
  def toJSON(self):
    import json
    import utils
    return json.dumps(dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]]), ensure_ascii=False, cls=utils.MyJsonEncoder)

# 时间段类，记录每个时间段已预约的人数
class Time_Bucket(models.Model):
  start_time = models.DateTimeField()
  occupation = models.PositiveIntegerField(default=0)
  shop = models.ForeignKey(Shop)

# 课程的可预约时间
class Bookable_Time(models.Model):
  course = models.ForeignKey(Course)
  start_time = models.DateTimeField()
  end_time = models.DateTimeField()
  occupation = models.PositiveIntegerField(default=0)
  def toJSON(self):
    import json
    import utils
    return json.dumps(dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]]), ensure_ascii=False, cls=utils.MyJsonEncoder)

# 服务类
class Service(models.Model):
  name = models.CharField(max_length=20)
  description = models.CharField(max_length=100)
  price = models.PositiveIntegerField(default=0)
  shop = models.ForeignKey(Shop)

# 订单类型枚举
ORDER_TYPE = ((1, u'site'), (2, u'course'))
# 订单状态枚举
ORDER_STATE = ((1, u'to_pay'), (2, u'cancel'), (3, u'time_out'), (4, u'success'))
# 订单类
class Order(models.Model):
  oid = models.CharField(max_length=32, unique=True)
  create_time = models.DateTimeField(auto_now_add=True)
  pay_time = models.DateTimeField(null=True)
  finish_time = models.DateTimeField(null=True)
  user = models.ForeignKey(User)
  price = models.PositiveIntegerField()
  course = models.ForeignKey(Course, null=True)
  order_type = models.CharField(max_length=10, choices=ORDER_TYPE)
  coupons = models.ForeignKey(Coupon, null=True)
  start_time = models.DateTimeField()
  end_time = models.DateTimeField()
  people_amount = models.PositiveIntegerField(default=1)
  services = models.TextField(null=True)
  state = models.CharField(max_length=20, choices=ORDER_STATE, default=1)
  shop = models.ForeignKey(Shop)
  def __unicode__(self):
    return '%s->%s' % (self.user.id, self.create_time)

# from http://www.pythonfan.org/thread-7614-1-1.html
class SAEFieldFile(FieldFile):
  def getUploadTo(self):
    return self.upload_to

  def save(self, name, content, save=True):
    name = self.field.generate_filename(self.instance, name)
    #for SAE
    s = sae.storage.Client()
    ob = sae.storage.Object(content._get_file().read())
    url = s.put('images', name, ob)
    self.name = name
    setattr(self.instance, self.field.name, self.name)

    # Update the filesize cache
    self._size = content.size
    self._committed = True

    # Save the object because it has changed, unless save is False
    #if save:
    #    self.instance.save()

class SAEImageFieldFile(ImageFile, SAEFieldFile):
  def delete(self, save=True):
    # Clear the image dimensions cache
    if hasattr(self, '_dimensions_cache'):
      del self._dimensions_cache
    super(ImageFieldFile, self).delete(save)

class ZGImageFieldFile(SAEImageFieldFile):
  def save(self, name, content, save=True):
    super(SAEImageFieldFile, self).save(name, content, save=True)

class ZGImageField(ImageField):
  attr_class = ZGImageFieldFile
  def __init__(self, verbose_name=None, name=None, width_field=None, height_field=None, **kwargs):
    super(ZGImageField, self).__init__(verbose_name, name, **kwargs)

############################
remote = not environ.get("APP_NAME", "")
if not remote:
  ImageField = ZGImageField
############################

class Image(models.Model):
  url = ImageField(upload_to = 'images/')