# Generated by Django 2.2.2 on 2019-07-29 09:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0020_cartitems_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Orders',
        ),
    ]
