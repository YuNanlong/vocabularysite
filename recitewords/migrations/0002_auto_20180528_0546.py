# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import recitewords.models


class Migration(migrations.Migration):

    dependencies = [
        ('recitewords', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wordbook',
            name='front_image',
            field=models.ImageField(default='bookfront/default.jpg', upload_to=recitewords.models.bookfront_upload_path),
        ),
    ]
