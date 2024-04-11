from django.contrib import admin

from .models import *
from ckeditor.widgets import CKEditorWidget
from django.db import models
from django.utils.safestring import mark_safe

class NewsAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget}
    }
    list_display = ['title', 'image_display', 'created_at']  # Specify fields to display in the admin list view
    readonly_fields = ('image_display',)  # Make the image_display field read-only

    def image_display(self, obj):
        # Custom method to display the image in the admin interface
        if obj.image:
            return mark_safe('<img src="{}" width="50px" height="50px" />'.format(obj.image.url))
        else:
            return 'No Image'

    image_display.allow_tags = True  # Allow HTML tags in the output (for displaying images)
    image_display.short_description = 'Image'  # Set a custom column header for the image

admin.site.register(New, NewsAdmin)