# Generated by Django 2.2.2 on 2019-07-15 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0016_auto_20190715_1922'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadedfile',
            name='saved_path',
            field=models.CharField(max_length=500, null=True),
        ),
    ]
