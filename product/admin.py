from django.contrib import admin
from .models import *
from django.utils.html import format_html

class TimeStampedModelAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'composition','description', 'display_image', 'manufacturer', 'quantity_available', 'expiry_date', 'category', 'product_type')

    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="150" />'.format(obj.image.url))
        else:
            return 'No Image'

    display_image.allow_tags = True


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductType, TimeStampedModelAdmin)
admin.site.register(Manufacturer, TimeStampedModelAdmin)
admin.site.register(Category, TimeStampedModelAdmin)
admin.site.register(CompositionUnit, TimeStampedModelAdmin)
admin.site.register(Generic, TimeStampedModelAdmin)
admin.site.register(PackSizeUnit, TimeStampedModelAdmin)





