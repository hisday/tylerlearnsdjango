# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-02-26 04:48
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_post_tag2'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='tag2',
        ),
    ]