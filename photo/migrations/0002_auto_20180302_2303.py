# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-03-02 14:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='image',
            field=models.ImageField(upload_to='photo/%Y/%m'),
        ),
    ]
