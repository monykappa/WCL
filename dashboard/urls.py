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
    
    # User
    path('dashboard/user/', views.UserView.as_view(), name='user'),
    path('edit_user/<int:user_id>/', views.EditUserView.as_view(), name='edit_user'),
    path('dashboard/delete_user/<int:user_id>/', views.DeleteUserView.as_view(), name='delete_user'),
    
    # Dashboard
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    
    
    # Products
    path('dashboard/products/', views.ProductsView.as_view(), name='products'),
    path('dashboard/get_product_details/<int:product_id>/', views.ProductDetailsView.as_view(), name='get_product_details'),
    path('products/edit/<slug:slug>/', views.EditProductView.as_view(), name='edit_product'),
    path('products/delete/<slug:slug>/', views.DeleteProductView.as_view(), name='delete_product'),
    

    # Export to excel
    path('dashboard/export/', views.ExportToExcelView.as_view(), name='export_to_excel'),
    
    
    # Category
    path('dashboard/category/', views.CategoryView.as_view(), name='category'),
    path('dashboard/category/edit/<slug:category_slug>/', views.EditCategoryView.as_view(), name='edit_category'),
    path('dashboard/category/<int:category_id>/delete/', views.DeleteCategoryView.as_view(), name='delete_category'),
    
    
    # Manufacturer
    path('dashboard/manufacturer/', views.ManufacturerView.as_view(), name='manufacturer'),
    path('dashboard/manufacturers/edit/<slug:manufacturer_slug>/', views.EditManufacturerView.as_view(), name='edit_manufacturer'),
    path('manufacturers/<int:manufacturer_id>/delete/', views.DeleteManufacturerView.as_view(), name='delete_manufacturer'),
    
    # product Type
    path('dashboard/product_type/', views.ProductTypeView.as_view(), name='product_type'),
    path('dashboard/edit_product_type/edit/<slug:slug>/', views.EditProductTypeView.as_view(), name='edit_product_type'),
    path('delete_product_type/<int:drug_type_id>/', views.DeleteProductTypeView.as_view(), name='delete_product_type'),
    
    # News
    path('dashboard/news/', views.NewsView.as_view(), name='news'),
    path('dashboard/add_news/', views.AddNewsView.as_view(), name='add_news'),
    path('dashboard/news/edit/<slug:new_slug>/', views.EditNewsView.as_view(), name='edit_news'),
    path('delete_news/<int:new_id>/', views.DeleteNewsView.as_view(), name='delete_news'),
    path('dashboard/news/update-history/<slug:new_slug>/', views.UpdateHistoryView.as_view(), name='update_history'),
    

    # Gallery
    path('gallery_list/', views.GalleryListView.as_view(), name='gallery_list'),
    path('gallery/edit/<slug:gallery_slug>/', views.UpdateGalleryView.as_view(), name='edit_gallery'),
    path('gallery/<int:gallery_id>/delete/', views.DeleteGalleryView.as_view(), name='delete_gallery'),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
