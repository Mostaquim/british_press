# Generated by Django 2.2.2 on 2019-07-26 15:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ordercart', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='salutation',
        ),
    ]
