# Generated by Django 2.2.2 on 2019-08-02 13:42

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wagtailcore', '0041_group_collection_permissions_verbose_name_plural'),
        ('wagtailimages', '0001_squashed_0021'),
        ('contenttypes', '0002_remove_content_type_name'),
        ('wagtailredirects', '0006_redirect_increase_max_length'),
        ('wagtailforms', '0003_capitalizeverbose'),
        ('formpage', '0007_auto_20190628_1731'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CatalogPage',
            new_name='FlyerPage',
        ),
    ]
