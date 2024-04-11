from django.contrib import admin
from .models import *
from django.utils.html import format_html

class TimeStampedModelAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at')

class DrugAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'display_image', 'manufacturer', 'price', 'quantity_available', 'expiry_date', 'category', 'drug_type')

    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="150" />'.format(obj.image.url))
        else:
            return 'No Image'

    display_image.allow_tags = True

admin.site.register(Drug, DrugAdmin)
admin.site.register(DrugType, TimeStampedModelAdmin)
admin.site.register(Manufacturer, TimeStampedModelAdmin)
admin.site.register(Category, TimeStampedModelAdmin)

