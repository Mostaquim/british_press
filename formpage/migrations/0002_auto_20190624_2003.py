# Generated by Django 2.2.2 on 2019-06-24 14:03

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailforms', '0003_capitalizeverbose'),
        ('wagtailcore', '0041_group_collection_permissions_verbose_name_plural'),
        ('wagtailredirects', '0006_redirect_increase_max_length'),
        ('contenttypes', '0002_remove_content_type_name'),
        ('wagtailimages', '0001_squashed_0021'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('formpage', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='FormPage',
            new_name='CatalogPage',
        ),
    ]
