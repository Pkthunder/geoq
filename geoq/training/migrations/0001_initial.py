# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Training',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=250)),
                ('category', models.CharField(default=b'Uncategorized', max_length=120, null=True, help_text=b'Category of training, eg. FEMA', blank=True)),
                ('gamification_signals', models.CharField(help_text=b'After training which Signals should be sent to gamification server?', max_length=250, null=True, blank=True)),
                ('content_link', models.CharField(help_text=b'Link to PDF/PPT/training or web page for training that will open in a new window', max_length=500, null=True, blank=True)),
                ('quiz_data', jsonfield.fields.JSONField(help_text=b'If user should be quized after, list of questions and answers and percent_complete if not 100%', null=True, blank=True)),
                ('description', models.TextField(help_text=b'Details to show potential student.', null=True, blank=True)),
                ('updated_at', models.DateTimeField(help_text=b'Last updated time/date', auto_now=True)),
                ('private', models.BooleanField(default=False, help_text=b'Check to hide in public list')),
                ('primary_contact', models.ForeignKey(help_text=b'Contact for training.', to=settings.AUTH_USER_MODEL)),
                ('users_completed', models.ManyToManyField(help_text=b'Users that completed this training.', related_name='users_completed', null=True, to=settings.AUTH_USER_MODEL, blank=True)),
            ],
        ),
    ]
