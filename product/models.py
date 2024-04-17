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
from django_countries.fields import CountryField
import pytz 
from django.utils.text import slugify




def validate_file_extension(value): 
    ext = os.path.splitext(value.name)[1]  
    valid_extensions = ['.png', '.jpg', '.jpeg', '.webp']
    if not ext.lower() in valid_extensions:
        raise ValidationError(u'Unsupported file extension.')

def images_directory_path(instance, filename):
    unique_id = str(uuid.uuid4())
    directory_path = f'content/{unique_id}/'
    return os.path.join(directory_path, filename)

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    class Meta:
        abstract = True

def generate_slug(value):
    return slugify(value)

class DrugType(TimeStampedModel):
    name = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    slug = models.SlugField(unique=True, max_length=100, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_slug(self.name)  # Generate slug from the name field
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Manufacturer(TimeStampedModel):
    name = models.CharField(max_length=100, null=True, blank=True)
    country = CountryField()
    description = models.CharField(max_length=500, null=True, blank=True)
    slug = models.SlugField(unique=True, max_length=100, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)  # Generate slug from the name fizeld
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Category(TimeStampedModel):
    name = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    slug = models.SlugField(unique=True, max_length=100, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_slug(self.name) 
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Drug(TimeStampedModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to=images_directory_path, validators=[validate_file_extension], blank=True, null=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_available = models.PositiveIntegerField(default=0)
    expiry_date = models.DateField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    drug_type = models.ForeignKey(DrugType, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_slug(self.name)  # Generate unique slug from the name field
        super().save(*args, **kwargs)


    def __str__(self):
        return self.name