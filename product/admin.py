from django.contrib import admin
from .models import *
from django.utils.html import format_html

class TimeStampedModelAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'manufacturer', 'get_composition', 'get_pack_size', 'description', 'display_image', 'category', 'product_type')

    def get_composition(self, obj):
        return ", ".join([str(comp) for comp in obj.compositions.all()])
    get_composition.short_description = 'Compositions'

    def get_pack_size(self, obj):
        return ", ".join([str(size) for size in obj.pack_sizes.all()])
    get_pack_size.short_description = 'Pack Sizes'

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
admin.site.register(Composition, TimeStampedModelAdmin)
admin.site.register(PackSize, TimeStampedModelAdmin)





