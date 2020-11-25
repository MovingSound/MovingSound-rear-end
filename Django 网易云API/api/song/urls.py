from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('url', views.url),
]
