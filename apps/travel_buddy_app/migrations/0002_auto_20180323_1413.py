# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-03-23 18:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel_buddy_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='travel',
            name='travel_date_from',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='travel',
            name='travel_date_to',
            field=models.DateField(),
        ),
    ]
