# Generated by Django 3.0.2 on 2020-08-16 22:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_buy_order_no'),
    ]

    operations = [
        migrations.AddField(
            model_name='buy',
            name='datetimefield',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 8, 16, 22, 55, 9, 617533)),
        ),
    ]
