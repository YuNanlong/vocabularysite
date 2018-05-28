# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import recitewords.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DailyProgress',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('learn_date', models.DateField()),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DailyTask',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('update_date', models.DateField()),
                ('is_finished', models.BooleanField(default=False)),
                ('task_id', models.IntegerField(null=True)),
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
                ('spelling', models.CharField(max_length=255, unique=True)),
                ('meaning', models.TextField()),
                ('past_tense', models.CharField(max_length=64)),
                ('past_priciple', models.CharField(max_length=64)),
                ('present_progressive', models.CharField(max_length=64)),
                ('plurality', models.CharField(max_length=64)),
                ('example', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='WordBook',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=128, unique=True)),
                ('description', models.TextField()),
                ('front_image', models.ImageField(default='bookfront/default.jpg', upload_to=recitewords.models.bookfront_upload_path, width_field=531, height_field=387)),
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
        migrations.AddField(
            model_name='dailyprogress',
            name='word',
            field=models.ForeignKey(to='recitewords.WordSet'),
        ),
    ]
