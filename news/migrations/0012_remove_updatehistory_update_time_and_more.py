# Generated by Django 5.0.3 on 2024-04-13 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0011_updatehistory_previous_update_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='updatehistory',
            name='update_time',
        ),
        migrations.AddField(
            model_name='updatehistory',
            name='new_update_time',
            field=models.DateTimeField(null=True),
        ),
    ]