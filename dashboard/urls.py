from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path as url
from django.shortcuts import render 
from . import views
from django.conf import settings 


app_name = 'dashboard'
urlpatterns = [
    path('dashboard_base/', views.dashboard_base, name='dashboard_base'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/products/', views.products, name='products'),
    path('dashboard/manufacturer/', views.manufacturer, name='manufacturer'),
    
    
    #sign in 
    path('sign_in/', views.sign_in, name='sign_in'),

    #log out 
    path('logout/', views.logout_view, name='logout'),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
