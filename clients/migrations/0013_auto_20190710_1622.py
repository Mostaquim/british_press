# Generated by Django 2.2.2 on 2019-07-10 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0012_auto_20190710_1600'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitems',
            name='priceGross',
        ),
        migrations.RemoveField(
            model_name='cartitems',
            name='priceNet',
        ),
        migrations.RemoveField(
            model_name='cartitems',
            name='shippingGross',
        ),
        migrations.RemoveField(
            model_name='cartitems',
            name='shippingNet',
        ),
        migrations.AddField(
            model_name='cartitems',
            name='price_gross',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='cartitems',
            name='price_net',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='cartitems',
            name='shipping_gross',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='cartitems',
            name='shipping_net',
            field=models.FloatField(null=True),
        ),
    ]
