# Generated by Django 2.2.12 on 2021-06-15 15:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_auto_20210421_1008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buy',
            name='datetimefield',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 6, 15, 15, 0, 53, 469669)),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='datetimefield',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 6, 15, 15, 0, 53, 468571)),
        ),
    ]
