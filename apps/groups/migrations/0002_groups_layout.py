# Generated by Django 4.0.4 on 2022-05-28 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='groups',
            name='layout',
            field=models.IntegerField(default=1, help_text='1 => test', verbose_name='Layout'),
        ),
    ]