# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import userena.models
from django.conf import settings
import easy_thumbnails.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailDomain',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email_domain', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=250)),
                ('primary_contact', models.ForeignKey(help_text=b'Contact for org.', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserAuthorization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('authorized', models.BooleanField(help_text=b'Check this to approve member access.')),
                ('permission_granted_on', models.DateTimeField(auto_now_add=True)),
                ('user_accepted_terms_on', models.DateTimeField(null=True, blank=True)),
                ('permissions_granted_by', models.ForeignKey(related_name='permissions_granted_by', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mugshot', easy_thumbnails.fields.ThumbnailerImageField(help_text='A personal image displayed in your profile.', upload_to=userena.models.upload_to_mugshot, verbose_name='mugshot', blank=True)),
                ('privacy', models.CharField(default=b'registered', help_text='Designates who can view your profile.', max_length=15, verbose_name='privacy', choices=[(b'open', 'Open'), (b'registered', 'Registered'), (b'closed', 'Closed')])),
                ('email', models.CharField(max_length=250, null=True, blank=True)),
                ('score', models.IntegerField(default=1)),
                ('openbadge_id', models.CharField(max_length=250, null=True, blank=True)),
                ('organization', models.ForeignKey(blank=True, to='accounts.Organization', help_text=b"If '------', no Organization records share the email domain.", null=True)),
                ('user', models.OneToOneField(verbose_name='user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
                'permissions': (('view_profile', 'Can view profile'),),
            },
        ),
        migrations.AddField(
            model_name='userauthorization',
            name='user_profile',
            field=models.OneToOneField(to='accounts.UserProfile'),
        ),
        migrations.AddField(
            model_name='emaildomain',
            name='organization',
            field=models.ForeignKey(to='accounts.Organization'),
        ),
        migrations.AlterUniqueTogether(
            name='organization',
            unique_together=set([('name', 'primary_contact')]),
        ),
    ]
