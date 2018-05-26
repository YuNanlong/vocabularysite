# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20180513_1701'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='exam_amount',
            field=models.IntegerField(default=0),
        ),
    ]
