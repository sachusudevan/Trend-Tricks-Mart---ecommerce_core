# Generated by Django 4.0.4 on 2022-05-30 15:47

import apps.product.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0002_alter_categories_image'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('groups', '0003_alter_groups_layout'),
        ('product', '0005_delete_products'),
    ]

    operations = [
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('thumbnail', models.ImageField(blank=True, default=apps.product.models.products_thumbnail_default_image, null=True, upload_to=apps.product.models.products_thumbnail_image, verbose_name='Thumbnail')),
                ('slug', models.SlugField(editable=False, unique=True, verbose_name='Slug')),
                ('price', models.FloatField(blank=True, null=True, verbose_name='Price')),
                ('discount_type', models.IntegerField(blank=True, null=True, verbose_name='Discount Type')),
                ('discount', models.IntegerField(blank=True, null=True, verbose_name='Discount')),
                ('discounted_price', models.FloatField(blank=True, null=True, verbose_name='Discounted Price')),
                ('sku', models.CharField(blank=True, max_length=100, null=True, verbose_name='SKU')),
                ('barcode', models.CharField(blank=True, max_length=255, null=True, unique=True, verbose_name='Barcode')),
                ('quantity', models.IntegerField(blank=True, null=True, verbose_name='Quantity')),
                ('is_backorders', models.BooleanField(blank=True, null=True, verbose_name='IsBackorders')),
                ('is_physical', models.BooleanField(blank=True, null=True, verbose_name='IsPhysical')),
                ('weight', models.CharField(blank=True, max_length=255, null=True, verbose_name='Weight')),
                ('width', models.IntegerField(blank=True, null=True, verbose_name='Width')),
                ('height', models.IntegerField(blank=True, null=True, verbose_name='Height')),
                ('length', models.IntegerField(blank=True, null=True, verbose_name='Length')),
                ('status', models.IntegerField(blank=True, null=True, verbose_name='Status')),
                ('publishing_date', models.DateTimeField(blank=True, null=True, verbose_name='Publishing Date')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Created Date')),
                ('modified_date', models.DateTimeField(auto_now=True, verbose_name='Modified Date')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='categories.categories')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='groups.groups')),
                ('manufacture', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.manufactures')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
                'ordering': ('id',),
            },
        ),
    ]