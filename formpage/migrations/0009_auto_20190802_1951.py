# Generated by Django 2.2.2 on 2019-08-02 13:51

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('wagtailforms', '0003_capitalizeverbose'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wagtailimages', '0001_squashed_0021'),
        ('wagtailcore', '0041_group_collection_permissions_verbose_name_plural'),
        ('wagtailredirects', '0006_redirect_increase_max_length'),
        ('formpage', '0008_auto_20190802_1942'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='FlyerPage',
            new_name='CatalogPage',
        ),
    ]
