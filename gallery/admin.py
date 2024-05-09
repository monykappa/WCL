from django.contrib import admin
from django.contrib.admin import TabularInline
from .models import *


class ImageInline(admin.TabularInline):
    model = Image
    extra = 3

class ImageAdmin(admin.ModelAdmin):
    list_display = ('caption', 'date_added')

class GalleryAdmin(admin.ModelAdmin):
    inlines = [ImageInline]
    list_display = ('name', 'description')
    search_fields = ['name']

admin.site.register(Gallery, GalleryAdmin)
admin.site.register(Image, ImageAdmin)
