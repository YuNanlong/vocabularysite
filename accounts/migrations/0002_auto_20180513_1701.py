# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recitewords', '0001_initial'),
        ('accounts', '0001_initial'),
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='current_wordbook',
            field=models.ForeignKey(null=True, to='recitewords.WordBook'),
        ),
        migrations.AddField(
            model_name='user',
            name='daily_task_words',
            field=models.ManyToManyField(related_name='user_daily_task_words', to='recitewords.WordSet', through='recitewords.DailyTask'),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(verbose_name='groups', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group'),
        ),
        migrations.AddField(
            model_name='user',
            name='learned_words',
            field=models.ManyToManyField(related_name='user_learned_words', to='recitewords.WordSet', through='recitewords.LearnedWord'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(verbose_name='user permissions', blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission'),
        ),
    ]
