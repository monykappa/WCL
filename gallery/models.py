from django.db import models
from product.models import *
from django.core.exceptions import ValidationError
import os
import uuid


def validate_file_extension(value): 
    ext = os.path.splitext(value.name)[1]  
    valid_extensions = ['.png', '.jpg', '.jpeg', '.webp']
    if not ext.lower() in valid_extensions:
        raise ValidationError(u'Unsupported file extension.')

def images_directory_path(instance, filename):
    unique_id = str(uuid.uuid4())
    directory_path = f'gallery_images/{unique_id}/'
    return os.path.join(directory_path, filename)


class Gallery(TimeStampedModel, SlugMixin):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

class Image(models.Model):
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='gallery_images/', validators=[validate_file_extension], blank=True, null=True)
    caption = models.CharField(max_length=255, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    