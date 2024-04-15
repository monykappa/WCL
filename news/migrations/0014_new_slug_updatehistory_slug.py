# Generated by Django 5.0.3 on 2024-04-15 05:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0013_remove_updatehistory_new_update_time_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='new',
            name='slug',
            field=models.SlugField(blank=True, max_length=100, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='updatehistory',
            name='slug',
            field=models.SlugField(blank=True, max_length=100, null=True, unique=True),
        ),
    ]
