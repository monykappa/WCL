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
    #sign in 
    path('sign_in/', views.SignInView.as_view(), name='sign_in'),
    
    #log out 
    path('logout/', views.LogoutView.as_view(), name='logout'),
    
    
    # Dashboard
    # path('dashboard_base/', views.dashboard_base, name='dashboard_base'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    
    
    # Products
    path('dashboard/products/', views.ProductsView.as_view(), name='products'),
    
    
    # Category
    path('dashboard/category/', views.CategoryView.as_view(), name='category'),
    path('dashboard/category/edit/<slug:category_slug>/', views.EditCategoryView.as_view(), name='edit_category'),
    path('dashboard/category/<int:category_id>/delete/', views.DeleteCategoryView.as_view(), name='delete_category'),
    # path('dashboard/add_category/', views.AddCategoryView.as_view(), name='add_category'),
    
    
    # Manufacturer
    path('dashboard/manufacturer/', views.ManufacturerView.as_view(), name='manufacturer'),
    path('dashboard/manufacturers/edit/<slug:manufacturer_slug>/', views.EditManufacturerView.as_view(), name='edit_manufacturer'),
    path('manufacturers/<int:manufacturer_id>/delete/', views.DeleteManufacturerView.as_view(), name='delete_manufacturer'),
    # path('dashboard/add_manufacturer/', views.AddManufacturerView.as_view(), name='add_manufacturer'),
    
    # product Type
    path('dashboard/product_type/', views.ProductTypeView.as_view(), name='product_type'),
    # path('dashboard/add_product_type/', views.AddProductTypeView.as_view(), name='add_product_type'),
    path('dashboard/edit_product_type/edit/<slug:slug>/', views.EditProductTypeView.as_view(), name='edit_product_type'),
    path('delete_product_type/<int:drug_type_id>/', views.DeleteProductTypeView.as_view(), name='delete_product_type'),
    
    # News
    path('dashboard/news/', views.NewsView.as_view(), name='news'),
    path('dashboard/add_news/', views.AddNewsView.as_view(), name='add_news'),
    path('dashboard/news/edit/<slug:new_slug>/', views.EditNewsView.as_view(), name='edit_news'),
    path('delete_news/<int:new_id>/', views.DeleteNewsView.as_view(), name='delete_news'),
    path('dashboard/news/update-history/<slug:new_slug>/', views.UpdateHistoryView.as_view(), name='update_history'),
    

]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
