# Generated by Django 5.0.3 on 2024-04-13 10:14

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0012_remove_updatehistory_update_time_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='updatehistory',
            name='new_update_time',
        ),
        migrations.RemoveField(
            model_name='updatehistory',
            name='previous_update_time',
        ),
        migrations.AddField(
            model_name='updatehistory',
            name='update_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
