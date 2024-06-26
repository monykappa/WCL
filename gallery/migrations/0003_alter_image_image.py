# Generated by Django 5.0.4 on 2024-05-09 15:28

import gallery.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0002_alter_image_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='gallery_images/', validators=[gallery.models.validate_file_extension]),
        ),
    ]
