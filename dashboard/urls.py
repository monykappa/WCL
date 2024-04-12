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
    
    
    # Category
    path('dashboard/category/', views.category, name='category'),
    path('dashboard/category/<int:category_id>/edit/', views.edit_category, name='edit_category'),
    path('categories/<int:category_id>/delete/', views.delete_category, name='delete_category'),
    path('add_category/', views.add_category, name='add_category'),
    
    
    # Manufacturer
    path('dashboard/manufacturer/', views.manufacturer, name='manufacturer'),
    path('dashboard/manufacturers/<int:manufacturer_id>/edit/', views.edit_manufacturer, name='edit_manufacturer'),
    path('manufacturers/<int:manufacturer_id>/delete/', views.delete_manufacturer, name='delete_manufacturer'),
    path('dashboard/add_manufacturer/', views.add_manufacturer, name='add_manufacturer'),
    
    # product Type
    path('dashboard/product_type/', views.product_type, name='product_type'),
    path('dashboard/add_product_type/', views.add_product_type, name='add_product_type'),
    path('dashboard/edit_product_type/<int:drug_type_id>/', views.edit_product_type, name='edit_product_type'),
    path('delete_product_type/<int:drug_type_id>/', views.delete_product_type, name='delete_product_type'),
    
    # News
    path('dashboard/news/', views.news, name='news'),
    
    #sign in 
    path('sign_in/', views.sign_in, name='sign_in'),

    #log out 
    path('logout/', views.logout_view, name='logout'),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)