# Generated by Django 2.2.2 on 2019-07-29 10:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ordercart', '0003_auto_20190729_1556'),
    ]

    operations = [
        migrations.RenameField(
            model_name='address',
            old_name='house_number',
            new_name='houseNumber',
        ),
    ]
