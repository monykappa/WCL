from django.db import models
from django.db import models
from django.contrib.auth.models import User 
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from ckeditor.fields import RichTextField
import uuid
from decimal import Decimal
from django.utils import timezone
import os
from datetime import datetime, date


def validate_file_extension(value): 
    ext = os.path.splitext(value.name)[1]  
    valid_extensions = ['.png', '.jpg', '.jpeg', '.webp']
    if not ext.lower() in valid_extensions:
        raise ValidationError(u'Unsupported file extension.')

def images_directory_path(instance, filename):
    unique_id = str(uuid.uuid4())
    directory_path = f'content/{unique_id}/'
    return os.path.join(directory_path, filename)


class New(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to=images_directory_path, validators=[validate_file_extension], blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    update_count = models.IntegerField(default=0)
    is_published = models.BooleanField(default=False) 

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.pk:
            self.update_count += 1
        super(New, self).save(*args, **kwargs)
        
        
class UpdateHistory(models.Model):
    news = models.ForeignKey('New', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    update_time = models.DateTimeField(auto_now_add=True)
    title_before = models.CharField(max_length=100, null=True, blank=True)
    image_before = models.ImageField(upload_to=images_directory_path, validators=[validate_file_extension], null=True, blank=True)
    description_before = models.TextField(null=True, blank=True)
    title_after = models.CharField(max_length=100,null=True, blank=True)
    image_after = models.ImageField(upload_to=images_directory_path, validators=[validate_file_extension], null=True, blank=True)
    description_after = models.TextField()

    def __str__(self):
        return f"{self.news.title} - {self.update_time}"

    
