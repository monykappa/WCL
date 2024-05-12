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
    # path('base/', views.BaseView.as_view(), name='base'),
    path('', views.HomeView.as_view(), name='home'),
    path('about_us/', views.AboutUsView.as_view(), name='about_us'),
    path('contact_us/', views.ContactUsView.as_view(), name='contact_us'),
    path('ceo_message/', views.CeoMessageView.as_view(), name='ceo_message'),
    path('top_management/', views.TopManagementView.as_view(), name='top_management'),
    
    
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
