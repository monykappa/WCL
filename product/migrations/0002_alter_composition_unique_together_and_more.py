# Generated by Django 5.0.4 on 2024-05-10 08:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='composition',
            unique_together={('value', 'composition_unit')},
        ),
        migrations.AlterUniqueTogether(
            name='packsize',
            unique_together={('value', 'pack_size_unit')},
        ),
    ]