# Generated by Django 2.2.2 on 2019-06-24 14:47

from django.db import migrations, models
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('formpage', '0003_listitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='catalogpage',
            name='content',
            field=wagtail.core.fields.RichTextField(null=True),
        ),
        migrations.AddField(
            model_name='listitem',
            name='text',
            field=models.CharField(max_length=500, null=True),
        ),
    ]
