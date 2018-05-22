# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DailyTask',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('updata_date', models.DateField()),
                ('is_new', models.BooleanField()),
                ('is_finished', models.BooleanField(default=False)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LearnedWord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('mastery_degree', models.IntegerField(default=0)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('spelling', models.CharField(max_length=256, unique=True)),
                ('meaning', models.TextField()),
                ('simple_meaning', models.TextField()),
                ('wrong_meaning_1', models.TextField()),
                ('wrong_meaning_2', models.TextField()),
                ('wrong_meaning_3', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='WordBook',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=128, unique=True)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='WordSet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('word', models.ForeignKey(to='recitewords.Word')),
                ('wordbook', models.ForeignKey(to='recitewords.WordBook')),
            ],
        ),
        migrations.AddField(
            model_name='wordbook',
            name='words',
            field=models.ManyToManyField(to='recitewords.Word', through='recitewords.WordSet'),
        ),
        migrations.AddField(
            model_name='learnedword',
            name='word',
            field=models.ForeignKey(to='recitewords.WordSet'),
        ),
        migrations.AddField(
            model_name='dailytask',
            name='word',
            field=models.ForeignKey(to='recitewords.WordSet'),
        ),
    ]
