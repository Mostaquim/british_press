# Generated by Django 2.2.2 on 2019-07-17 11:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0018_uploadedfile_file_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadedfile',
            name='cart_item',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='files', to='clients.CartItems'),
        ),
    ]