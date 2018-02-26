# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-02-26 04:47
from __future__ import unicode_literals

from django.db import migrations
import tagging.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_post_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='tag2',
            field=tagging.fields.TagField(blank=True, max_length=255),
        ),
    ]
