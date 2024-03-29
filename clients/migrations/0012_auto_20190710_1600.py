# Generated by Django 2.2.2 on 2019-07-10 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0011_cartitems_prices'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitems',
            name='prices',
        ),
        migrations.AddField(
            model_name='cartitems',
            name='priceGross',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='cartitems',
            name='priceNet',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='cartitems',
            name='shippingGross',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='cartitems',
            name='shippingNet',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
    ]
