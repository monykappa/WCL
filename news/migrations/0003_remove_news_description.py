# Generated by Django 5.0.3 on 2024-04-09 06:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_rename_product_news'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='news',
            name='description',
        ),
    ]
