# Generated by Django 4.0.4 on 2022-05-29 11:44

import apps.categories.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categories',
            name='image',
            field=models.ImageField(blank=True, default=apps.categories.models.category_default_image, null=True, upload_to=apps.categories.models.category_image, verbose_name='Image'),
        ),
    ]
