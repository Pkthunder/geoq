# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields
import django.contrib.gis.db.models.fields
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(default=b'In work', max_length=15, choices=[(b'Unassigned', b'Unassigned'), (b'In work', b'In work'), (b'Awaiting review', b'Awaiting review'), (b'In review', b'In review'), (b'Completed', b'Completed')])),
                ('properties', jsonfield.fields.JSONField(null=True, blank=True)),
                ('the_geom', django.contrib.gis.db.models.fields.GeometryField(srid=4326, null=True, blank=True)),
                ('analyst', models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL)),
                ('aoi', models.ForeignKey(related_name='features', editable=False, to='core.AOI')),
                ('job', models.ForeignKey(editable=False, to='core.Job')),
                ('project', models.ForeignKey(editable=False, to='core.Project')),
            ],
            options={
                'ordering': ('-updated_at', 'aoi'),
            },
        ),
        migrations.CreateModel(
            name='FeatureType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('type', models.CharField(max_length=25, choices=[(b'Point', b'Point'), (b'LineString', b'Line'), (b'Polygon', b'Polygon')])),
                ('category', models.CharField(default=b'', max_length=25, null=True, help_text=b"An optional group to make finding this feature type easier. e.g. 'FEMA'", blank=True)),
                ('order', models.IntegerField(default=0, help_text=b'Optionally specify the order features should appear on the edit menu. Lower numbers appear sooner.', null=True, blank=True)),
                ('properties', jsonfield.fields.JSONField(help_text=b'Metadata added to properties of individual features. Should be in JSON format, e.g. {"severity":"high", "mapText":"Text to Show instead of icon"}', null=True, blank=True)),
                ('style', jsonfield.fields.JSONField(help_text=b'Any special CSS style that features of this types should have. e.g. {"opacity":0.7, "color":"red", "backgroundColor":"white", "mapTextStyle":"white_overlay", "iconUrl":"path/to/icon.png"}', null=True, blank=True)),
                ('icon', models.ImageField(help_text=b'Upload an icon (now only in Admin menu) of the FeatureType here, will override style iconUrl if set', null=True, upload_to=b'static/featuretypes/', blank=True)),
            ],
            options={
                'ordering': ['-category', 'order', 'name', 'id'],
            },
        ),
        migrations.CreateModel(
            name='GeoeventsSource',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('url', models.URLField(help_text=b'URL of service location. Requires JSONP support', max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Layer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'Name that will be displayed within GeoQ', max_length=200)),
                ('type', models.CharField(max_length=75, choices=[(b'WMS', b'WMS'), (b'KML', b'KML'), (b'GeoRSS', b'GeoRSS'), (b'ESRI Identifiable MapServer', b'ESRI Identifiable MapServer'), (b'ESRI Tiled Map Service', b'ESRI Tiled Map Service'), (b'ESRI Dynamic Map Layer', b'ESRI Dynamic Map Layer'), (b'ESRI Feature Layer', b'ESRI Feature Layer'), (b'GeoJSON', b'GeoJSON'), (b'ESRI Clustered Feature Layer', b'ESRI Clustered Feature Layer'), (b'GPX', b'GPX'), (b'WMTS', b'WMTS'), (b'Social Networking Link', b'Social Networking Link'), (b'Web Data Link', b'Web Data Link'), (b'Bing', b'Bing'), (b'Google Maps', b'Google Maps'), (b'Yandex', b'Yandex'), (b'Leaflet Tile Layer', b'Leaflet Tile Layer')])),
                ('url', models.CharField(help_text=b'URL of service. If WMS or ESRI, can be any valid URL. Otherwise, the URL will require a local proxy', max_length=500)),
                ('layer', models.CharField(help_text=b'Layer names can sometimes be comma-separated, and are not needed for data layers (KML, GeoRSS, GeoJSON...)', max_length=800, null=True, blank=True)),
                ('image_format', models.CharField(blank=True, max_length=75, null=True, help_text=b'The MIME type of the image format to use for tiles on WMS layers (image/png, image/jpeg image/gif...). Double check that the server exposes this exactly - some servers push png instead of image/png.', choices=[(b'image/png', b'image/png'), (b'image/png8', b'image/png8'), (b'image/png24', b'image/png24'), (b'image/jpeg', b'image/jpeg'), (b'image/gif', b'image/gif'), (b'image/tiff', b'image/tiff'), (b'image/tiff8', b'image/tiff8'), (b'image/geotiff', b'image/geotiff'), (b'image/geotiff8', b'image/geotiff8'), (b'image/svg', b'image/svg'), (b'rss', b'rss'), (b'kml', b'kml'), (b'kmz', b'kmz'), (b'json', b'json'), (b'png', b'png'), (b'png8', b'png8'), (b'png24', b'png24'), (b'jpeg', b'jpeg'), (b'jpg', b'jpg'), (b'gif', b'gif'), (b'tiff', b'tiff'), (b'tiff8', b'tiff8'), (b'geotiff', b'geotiff'), (b'geotiff8', b'geotiff8'), (b'svg', b'svg')])),
                ('styles', models.CharField(help_text=b'The name of a style to use for this layer (only useful for WMS layers if the server exposes it.)', max_length=200, null=True, blank=True)),
                ('transparent', models.BooleanField(default=True, help_text=b'If WMS or overlay, should the tiles be transparent where possible?')),
                ('refreshrate', models.PositiveIntegerField(help_text=b'Layer refresh rate in seconds for vector/data layers (will not refresh WMS layers)', null=True, verbose_name=b'Layer Refresh Rate', blank=True)),
                ('description', models.TextField(help_text=b'Text to show in layer chooser, please be descriptive - this will soon be searchable', max_length=800, null=True, blank=True)),
                ('attribution', models.CharField(help_text=b'Attribution from layers to the map display (will show in bottom of map when layer is visible).', max_length=200, null=True, blank=True)),
                ('token', models.CharField(help_text=b'Authentication token, if required (usually only for secure layer servers)', max_length=400, null=True, blank=True)),
                ('extent', django.contrib.gis.db.models.fields.PolygonField(help_text=b'Extent of the layer.', srid=4326, null=True, blank=True)),
                ('layer_parsing_function', models.CharField(help_text=b'Advanced - The javascript function used to parse a data service (GeoJSON, GeoRSS, KML), needs to be an internally known parser. Contact an admin if you need data parsed in a new way.', max_length=100, null=True, blank=True)),
                ('enable_identify', models.BooleanField(default=False, help_text=b'Advanced - Allow user to click map to query layer for details. The map server must support queries for this layer.')),
                ('info_format', models.CharField(blank=True, max_length=75, null=True, help_text=b'Advanced - what format the server returns for an WMS-I query', choices=[(b'application/vnd.ogc.wms_xml', b'application/vnd.ogc.wms_xml'), (b'application/xml', b'application/xml'), (b'text/html', b'text/html'), (b'text/plain', b'text/plain')])),
                ('root_field', models.CharField(help_text=b'Advanced - For WMS-I (queryable) layers, the root field returned by server. Leave blank for default (will usually be "FIELDS" in returned XML).', max_length=100, null=True, blank=True)),
                ('fields_to_show', models.CharField(help_text=b'Fields to show when someone uses the identify tool to click on the layer. Leave blank for all.', max_length=200, null=True, blank=True)),
                ('downloadableLink', models.URLField(help_text=b'URL of link to supporting tool (such as a KML document that will be shown as a download button)', max_length=400, null=True, blank=True)),
                ('layer_params', jsonfield.fields.JSONField(help_text=b'JSON key/value pairs to be sent to the web service.  ex: {"crs":"urn:ogc:def:crs:EPSG::4326"}', null=True, blank=True)),
                ('spatial_reference', models.CharField(default=b'EPSG:4326', max_length=32, null=True, help_text=b'The spatial reference of the service.  Should be in ESPG:XXXX format.', blank=True)),
                ('constraints', models.TextField(help_text=b'Constrain layer data displayed to certain feature types', null=True, blank=True)),
                ('disabled', models.BooleanField(default=False, help_text=b"If unchecked, Don't show this layer when listing all layers")),
                ('layer_info_link', models.URLField(help_text=b'URL of info about the service, or a help doc or something', max_length=500, null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('additional_domains', models.TextField(help_text=b'Semicolon seperated list of additional domains for the layer. Only used if you want to cycle through domains for load-balancing', null=True, blank=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Map',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(unique=True, max_length=75)),
                ('description', models.TextField(max_length=800, null=True, blank=True)),
                ('zoom', models.IntegerField(default=5, help_text=b'Sets the default zoom level of the map.', null=True, blank=True)),
                ('projection', models.CharField(default=b'EPSG:4326', max_length=32, null=True, help_text=b'Set the default projection for layers added to this map. Note that the projection of the map is usually determined by that of the current baseLayer', blank=True)),
                ('center_x', models.FloatField(default=0.0, help_text=b'Sets the center x coordinate of the map.  Maps on event pages default to the location of the event.', null=True, blank=True)),
                ('center_y', models.FloatField(default=0.0, help_text=b'Sets the center y coordinate of the map.  Maps on event pages default to the location of the event.', null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='MapLayer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('shown', models.BooleanField(default=True)),
                ('stack_order', models.IntegerField()),
                ('opacity', models.FloatField(default=0.8)),
                ('is_base_layer', models.BooleanField(help_text=b'Only one Base Layer can be enabled at any given time.')),
                ('display_in_layer_switcher', models.BooleanField()),
                ('layer', models.ForeignKey(related_name='map_layer_set', to='maps.Layer')),
                ('map', models.ForeignKey(related_name='map_set', to='maps.Map')),
            ],
            options={
                'ordering': ['stack_order'],
            },
        ),
        migrations.AddField(
            model_name='feature',
            name='template',
            field=models.ForeignKey(to='maps.FeatureType', on_delete=django.db.models.deletion.PROTECT),
        ),
    ]
