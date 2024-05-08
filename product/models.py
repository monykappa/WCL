from django.db import models
from django.db import models
from django.contrib.auth.models import User 
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
# from ckeditor.fields import RichTextField
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

# Define the slug generator function
def generate_slug(value):
    base_slug = slugify(value)
    slug = base_slug
    counter = 1
    while Product.objects.filter(slug=slug).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1
    return slug

# Define a mixin class for generating slugs
class SlugMixin(models.Model):
    slug = models.SlugField(unique=True, max_length=100, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.name:  # Check if name is not empty
            self.slug = generate_slug(self.name)  # Generate slug from the name field
        super().save(*args, **kwargs)

    class Meta:
        abstract = True  # Set abstract to True so that this class is not directly used as a model

# Example usage of the SlugMixin in your models
class ProductType(TimeStampedModel, SlugMixin):
    name = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.name


class Manufacturer(TimeStampedModel, SlugMixin):
    name = models.CharField(max_length=100, null=True, blank=True)
    country = CountryField()
    description = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.name


class Category(TimeStampedModel, SlugMixin):
    name = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.name


class Product(TimeStampedModel, SlugMixin):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to=images_directory_path, validators=[validate_file_extension], blank=True, null=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_available = models.PositiveIntegerField(default=0)
    expiry_date = models.DateField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE)

    def __str__(self):
        return self.name