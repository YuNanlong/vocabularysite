# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recitewords', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DailyProgress',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('learn_date', models.DateField()),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('word', models.ForeignKey(to='recitewords.WordSet')),
            ],
        ),
        migrations.RenameField(
            model_name='dailytask',
            old_name='updata_date',
            new_name='update_date',
        ),
        migrations.RemoveField(
            model_name='dailytask',
            name='is_new',
        ),
        migrations.AddField(
            model_name='dailytask',
            name='task_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='word',
            name='spelling',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
