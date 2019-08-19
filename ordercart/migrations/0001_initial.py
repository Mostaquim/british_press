# Generated by Django 2.2.2 on 2019-07-26 15:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.CharField(max_length=255, null=True)),
                ('salutation', models.CharField(max_length=255, null=True)),
                ('street', models.CharField(max_length=500, null=True)),
                ('house_number', models.CharField(max_length=255, null=True)),
                ('phonePrefix', models.CharField(max_length=20, null=True)),
                ('phoneNumber', models.CharField(max_length=255, null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='address', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
