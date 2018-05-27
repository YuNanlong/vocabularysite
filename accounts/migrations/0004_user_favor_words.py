# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recitewords', '0002_auto_20180520_0550'),
        ('accounts', '0003_user_exam_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='favor_words',
            field=models.ManyToManyField(to='recitewords.WordSet'),
        ),
    ]
