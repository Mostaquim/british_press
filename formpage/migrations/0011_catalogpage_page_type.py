# Generated by Django 2.2.2 on 2019-08-05 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formpage', '0010_auto_20190805_1136'),
    ]

    operations = [
        migrations.AddField(
            model_name='catalogpage',
            name='page_type',
            field=models.CharField(choices=[('flyer', 'Flyers'), ('other', 'Others')], default='other', max_length=10),
        ),
    ]
