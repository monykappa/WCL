# Generated by Django 5.0.3 on 2024-04-13 09:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0008_rename_update_details_updatehistory_description_after_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Publish',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_published', models.BooleanField(default=False)),
                ('news', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='news.new')),
            ],
        ),
    ]
