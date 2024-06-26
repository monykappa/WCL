from django.contrib import admin
from django.urls import include, path
from django.conf import settings 
from django.conf.urls.static import static
from django.urls import re_path as url

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('home.urls')),
    path('', include('product.urls')),
    path('', include('dashboard.urls')),
    path('', include('news.urls')),
    path('', include('gallery.urls')),
    
    
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
