from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path as url
from django.shortcuts import render 
from . import views
from django.conf import settings 


app_name = 'product'
urlpatterns = [
    path('products/', views.ProductsView.as_view(), name='products'),
    # path('product_detail/', views.product_detail, name='product_detail'),
    path('product/category/<slug:category_slug>/', views.CategoryPageView.as_view(), name='category_page'),
]



if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
