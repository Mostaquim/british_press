# Generated by Django 2.2.2 on 2019-08-05 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formpage', '0009_auto_20190802_1951'),
    ]

    operations = [
        migrations.AlterField(
            model_name='catalogpage',
            name='api_value',
            field=models.TextField(null=True),
        ),
    ]
