from django.urls import path, re_path, include
from . import views

urlpatterns = [
    path('', views.home),
    path('song/', include('api.song.urls')),
    re_path(r'^search[/]*', include('api.search.urls')),
]
