from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path as url
from django.shortcuts import render 
from . import views
from django.conf import settings 




app_name = 'home'
urlpatterns = [
    path('base/', views.base, name='base'),
    path('', views.home, name='home'),
    path('about_us/', views.about_us, name='about_us'),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
