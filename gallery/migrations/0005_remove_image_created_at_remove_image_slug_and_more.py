# Generated by Django 5.0.4 on 2024-05-13 03:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0004_gallery_created_at_gallery_slug_gallery_updated_at_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='image',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='image',
            name='updated_at',
        ),
    ]
