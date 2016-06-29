# -*- coding: utf-8 -*-
from holicLab.models import *
import datetime
import random

now = datetime.datetime.now()

# 创建用户
for i in xrange(0, 50):
  bindDate = now + datetime.timedelta(days=random.randint(-100, 100))
  User.objects.create(nickname='user%d' % i, phone='1388888888%d' % random.randint(0, 9), bind_date=bindDate.date(), consumption=random.randint(50, 500))

# 创建商店
for i in xrange(0, 5):
  Shop.objects.create(name="shop%d" % i, description='商店%d的简介' % i, notice='商店%d的注意事项' % i, cover_type=1, cover='', location='商店%d的地址' % i, price=1000, capacity=10, invalide_times='', state=1)

# 创建密码
Password.objects.create(start_time=now, end_time=(now + datetime.timedelta(hours=1)), content='1j23')
