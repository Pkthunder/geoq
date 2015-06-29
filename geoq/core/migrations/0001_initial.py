# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields
import django.contrib.gis.db.models.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AOI',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('assignee_id', models.PositiveIntegerField(null=True)),
                ('active', models.BooleanField(default=True, help_text=b"Check to make project 'Active' and visible to all users. Uncheck this to 'Archive' the project")),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('properties', jsonfield.fields.JSONField(help_text=b'JSON key/value pairs associated with this object, e.g. {"usng":"18 S TJ 87308 14549", "favorite":"true"}', null=True, blank=True)),
                ('polygon', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
                ('priority', models.SmallIntegerField(default=5, max_length=1, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])),
                ('status', models.CharField(default=b'Unassigned', max_length=15, choices=[(b'Unassigned', b'Unassigned'), (b'Assigned', b'Assigned'), (b'In work', b'In work'), (b'Awaiting review', b'Awaiting review'), (b'In review', b'In review'), (b'Completed', b'Completed')])),
            ],
            options={
                'verbose_name': 'Area of Interest',
                'verbose_name_plural': 'Areas of Interest',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('assignee_id', models.PositiveIntegerField(null=True)),
                ('active', models.BooleanField(default=True, help_text=b"Check to make project 'Active' and visible to all users. Uncheck this to 'Archive' the project")),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('properties', jsonfield.fields.JSONField(help_text=b'JSON key/value pairs associated with this object, e.g. {"usng":"18 S TJ 87308 14549", "favorite":"true"}', null=True, blank=True)),
                ('progress', models.SmallIntegerField(max_length=2, null=True, blank=True)),
                ('grid', models.CharField(default=b'usng', help_text=b'Select usng for Jobs inside the US, otherwise use mgrs', max_length=5, choices=[(b'usng', b'usng'), (b'mgrs', b'mgrs')])),
                ('tags', models.CharField(help_text=b'Useful tags to search social media with', max_length=50, null=True, blank=True)),
                ('analysts', models.ManyToManyField(related_name='analysts', null=True, to=settings.AUTH_USER_MODEL, blank=True)),
                ('assignee_type', models.ForeignKey(to='contenttypes.ContentType', null=True)),
            ],
            options={
                'ordering': ('-created_at',),
                'permissions': (('assign_job', 'Assign Job'),),
            },
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'Short name of this organization', unique=True, max_length=200)),
                ('url', models.CharField(help_text=b'Link that users should be directed to if icon is clicked', max_length=600, null=True, blank=True)),
                ('icon', models.ImageField(help_text=b'Upload an icon of the organization here', null=True, upload_to=b'static/organizations/', blank=True)),
                ('show_on_front', models.BooleanField(default=False, help_text=b'Show on the front of the GeoQ App')),
                ('order', models.IntegerField(default=0, help_text=b'Optionally specify the order orgs should appear on the front page. Lower numbers appear sooner.', null=True, blank=True)),
            ],
            options={
                'ordering': ['order', 'name'],
                'verbose_name_plural': 'Organizations',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('active', models.BooleanField(default=True, help_text=b"Check to make project 'Active' and visible to all users. Uncheck this to 'Archive' the project")),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('properties', jsonfield.fields.JSONField(help_text=b'JSON key/value pairs associated with this object, e.g. {"usng":"18 S TJ 87308 14549", "favorite":"true"}', null=True, blank=True)),
                ('project_type', models.CharField(max_length=50, choices=[(b'Hurricane/Cyclone', b'Hurricane/Cyclone'), (b'Tornado', b'Tornado'), (b'Earthquake', b'Earthquake'), (b'Extreme Weather', b'Extreme Weather'), (b'Fire', b'Fire'), (b'Flood', b'Flood'), (b'Tsunami', b'Tsunami'), (b'Volcano', b'Volcano'), (b'Pandemic', b'Pandemic'), (b'Exercise', b'Exercise'), (b'Special Event', b'Special Event'), (b'Training', b'Training')])),
                ('private', models.BooleanField(default=False, help_text=b"Check this to make this project 'Private' and available only to users assigned to it.")),
                ('contributors', models.ManyToManyField(help_text=b'User that will be able to take on jobs.', related_name='contributors', null=True, to=settings.AUTH_USER_MODEL, blank=True)),
                ('project_admins', models.ManyToManyField(help_text=b'User that has admin rights to project.', related_name='project_admins', null=True, to=settings.AUTH_USER_MODEL, blank=True)),
            ],
            options={
                'ordering': ('-created_at',),
                'permissions': (('open_project', 'Open Project'), ('close_project', 'Close Project'), ('archive_project', 'Archive Project')),
            },
        ),
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'Name of site-wide variable', max_length=200)),
                ('value', jsonfield.fields.JSONField(help_text=b'Value of site-wide variable that scripts can reference - must be valid JSON', null=True, blank=True)),
            ],
        ),
    ]
