from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
  url(r'^login$', views.login),
  url(r'^shop$', views.shopHandler),
  url(r'^course$', views.courseHandler),
  url(r'^password$', views.passwordHandler),
  url(r'^member$', views.memberHandler),
  url(r'^coupon$', views.couponHandler),
)
