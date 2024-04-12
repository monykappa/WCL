# Generated by Django 5.0.3 on 2024-04-11 05:16

import product.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0007_rename_product_drug'),
    ]

    operations = [
        migrations.AddField(
            model_name='drug',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=product.models.images_directory_path, validators=[product.models.validate_file_extension]),
        ),
    ]