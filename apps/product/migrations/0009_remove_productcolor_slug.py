# Generated by Django 4.0.4 on 2022-06-05 14:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0008_metadata'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productcolor',
            name='slug',
        ),
    ]
