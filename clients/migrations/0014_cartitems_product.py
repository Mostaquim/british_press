# Generated by Django 2.2.2 on 2019-07-11 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0013_auto_20190710_1622'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitems',
            name='product',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
