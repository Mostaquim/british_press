# Generated by Django 2.2.2 on 2019-06-28 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='clients',
            name='salutation',
            field=models.CharField(max_length=5, null=True),
        ),
    ]
