# -*- coding: utf-8 -*-
from holicLab.models import *
import datetime
import random

now = datetime.datetime.now()


gender = ['f', 'm']
role = [1, 2]
# 创建用户
for i in xrange(0, 50):
  bindDate = now + datetime.timedelta(days=random.randint(-100, 100))
  User.objects.create(gender=random.choice(gender), role=random.choice(role), nickname='user%d' % i, phone='1388888888%d' % random.randint(0, 9), bind_date=bindDate.date(), consumption=random.randint(50, 500))

# 创建商店
for i in xrange(0, 5):
  Shop.objects.create(name="shop%d" % i, state=random.randint(1, 2), description='商店%d的简介' % i, notice='商店%d的注意事项' % i, cover_type=1, cover='["url(/media/images/1467177464_E._\\u7528\\u6237\\u7ba1\\u7406.png)"]', location='商店%d的地址' % i, price=1000, capacity=10, invalide_times='')

# 创建订单
shops = Shop.objects.all()
users = User.objects.all()
for i in xrange(0, 10):
  shop = random.choice(shops)
  user = random.choice(users)
  start_time = now + datetime.timedelta(hours=random.randint(-500, 500))
  end_time = start_time + datetime.timedelta(hours=1)
  pwdContent = '%d' % (random.randint(1000, 9999))
  pwd = Password.objects.create(start_time=start_time, end_time=end_time, content=pwdContent)
  order = Order()
  order.user = user
  order.price = random.randint(50, 200)
  order.order_type = 1
  order.password = pwd
  order.start_time = start_time
  order.end_time = end_time
  order.state = random.randint(1, 4)
  order.shop = shop
  order.save()

