from django.conf.urls import patterns, include, url
import views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
  url(r'^$', views.homeHandler),
  url(r'^shop$', views.shopHandler),
  url(r'^course$', views.courseHandler),
  url(r'^order$', views.orderHandler),
  url(r'^user$', views.userHandler),
)
