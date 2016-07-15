from django.conf.urls import patterns, include, url
import views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
  url(r'^/$', views.indexHandler),
  url(r'^/login$', views.loginHandler),
  url(r'^/logout$', views.logoutHandler),
  url(r'^/shop$', views.shopHandler),
  url(r'^/course$', views.courseHandler),
  url(r'^/member$', views.memberHandler),
  url(r'^/coupon$', views.couponHandler),
  url(r'^/order$', views.orderHandler),
  url(r'^/export$', views.exportHandler),
  url(r'^/upload$', views.uploadHandler),
)
