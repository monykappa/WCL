# Generated by Django 5.0.3 on 2024-04-09 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_remove_news_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
