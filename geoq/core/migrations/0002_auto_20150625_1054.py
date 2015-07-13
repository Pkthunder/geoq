# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('training', '0001_initial'),
        ('auth', '0006_require_contenttypes_0002'),
        ('maps', '0001_initial'),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='feature_types',
            field=models.ManyToManyField(to='maps.FeatureType', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='job',
            name='map',
            field=models.ForeignKey(blank=True, to='maps.Map', null=True),
        ),
        migrations.AddField(
            model_name='job',
            name='project',
            field=models.ForeignKey(related_name='project', to='core.Project'),
        ),
        migrations.AddField(
            model_name='job',
            name='required_courses',
            field=models.ManyToManyField(help_text=b'Courses that must be passed to open these cells', to='training.Training', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='job',
            name='reviewers',
            field=models.ManyToManyField(related_name='reviewers', null=True, to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AddField(
            model_name='job',
            name='teams',
            field=models.ManyToManyField(related_name='teams', null=True, to='auth.Group', blank=True),
        ),
        migrations.AddField(
            model_name='comment',
            name='aoi',
            field=models.ForeignKey(help_text=b'Associated AOI for comment', to='core.AOI'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, help_text=b'User who made comment', null=True),
        ),
        migrations.AddField(
            model_name='aoi',
            name='analyst',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, help_text=b'User assigned to work the workcell.', null=True),
        ),
        migrations.AddField(
            model_name='aoi',
            name='assignee_type',
            field=models.ForeignKey(to='contenttypes.ContentType', null=True),
        ),
        migrations.AddField(
            model_name='aoi',
            name='job',
            field=models.ForeignKey(related_name='aois', to='core.Job'),
        ),
        migrations.AddField(
            model_name='aoi',
            name='reviewers',
            field=models.ManyToManyField(help_text=b'Users that actually reviewed this work.', related_name='aoi_reviewers', null=True, to=settings.AUTH_USER_MODEL, blank=True),
        ),
    ]
