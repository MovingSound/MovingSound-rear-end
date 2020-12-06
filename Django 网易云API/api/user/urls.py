from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('login', views.login),
    path('sent', views.sent),
    path('verify', views.verify),
    path('checkphone', views.checkphone),
    path('register', views.register),
    path('initname', views.initname),
    path('rebind', views.rebind),
    path('logout', views.logout),
    path('status', views.status),
    path('refresh', views.refresh),
    path('likelist', views.likelist),
    path('detail', views.detail),
    path('playlist', views.playlist),
    path('album', views.album),
    path('signin', views.signin),
    path('fm', views.fm),
    path('trash', views.trash),
    path('subcount', views.subcount),
    path('record', views.record),
    path('radio', views.radio),
    path('dj', views.dj),
    path('follows', views.follows),
    path('fans', views.fans),
    path('event', views.event),
    path('events', views.events),
    path('event/forward', views.event_forward),
    path('event/del', views.event_del),
    path('event/share', views.event_share),
    path('follow', views.follow),
    path('cloud', views.cloud),
    path('cloud/detail', views.cloud_detail),
    path('cloud/del', views.cloud_del),
    path('setting', views.setting),
    path('getarea', views.getarea),
    path('update', views.update),
    path('star', views.star),
]
