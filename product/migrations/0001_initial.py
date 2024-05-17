# Generated by Django 5.0.4 on 2024-05-17 06:10

import django.db.models.deletion
import django_countries.fields
import product.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('slug', models.SlugField(blank=True, max_length=250, null=True, unique=True)),
                ('name', models.CharField(blank=True, max_length=250, null=True)),
                ('description', models.CharField(blank=True, max_length=500, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CompositionUnit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('slug', models.SlugField(blank=True, max_length=250, null=True, unique=True)),
                ('name', models.CharField(max_length=250)),
                ('description', models.CharField(blank=True, max_length=500, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Generic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('slug', models.SlugField(blank=True, max_length=250, null=True, unique=True)),
                ('name', models.CharField(max_length=250)),
                ('description', models.CharField(blank=True, max_length=500, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Manufacturer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('slug', models.SlugField(blank=True, max_length=250, null=True, unique=True)),
                ('name', models.CharField(blank=True, max_length=250, null=True)),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('description', models.CharField(blank=True, max_length=500, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PackSizeUnit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('slug', models.SlugField(blank=True, max_length=250, null=True, unique=True)),
                ('name', models.CharField(max_length=250)),
                ('description', models.CharField(blank=True, max_length=500, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProductType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('slug', models.SlugField(blank=True, max_length=250, null=True, unique=True)),
                ('name', models.CharField(blank=True, max_length=250, null=True)),
                ('description', models.CharField(blank=True, max_length=500, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Composition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('slug', models.SlugField(blank=True, max_length=250, null=True, unique=True)),
                ('value', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('composition_unit', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='product.compositionunit')),
            ],
            options={
                'unique_together': {('value', 'composition_unit')},
            },
        ),
        migrations.CreateModel(
            name='PackSize',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('slug', models.SlugField(blank=True, max_length=250, null=True, unique=True)),
                ('value', models.DecimalField(decimal_places=2, max_digits=10)),
                ('pack_size_unit', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='product.packsizeunit')),
            ],
            options={
                'unique_together': {('value', 'pack_size_unit')},
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True, max_length=250, null=True, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('image', models.ImageField(blank=True, null=True, upload_to=product.models.images_directory_path, validators=[product.models.validate_file_extension])),
                ('description', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.category')),
                ('compositions', models.ManyToManyField(blank=True, to='product.composition')),
                ('generics', models.ManyToManyField(blank=True, to='product.generic')),
                ('manufacturer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.manufacturer')),
                ('pack_sizes', models.ManyToManyField(blank=True, to='product.packsize')),
                ('product_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.producttype')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
