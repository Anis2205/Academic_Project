# Generated by Django 5.2.1 on 2025-07-21 01:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('greenapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diy',
            name='slug',
            field=models.SlugField(blank=True, max_length=200, unique=True),
        ),
    ]
