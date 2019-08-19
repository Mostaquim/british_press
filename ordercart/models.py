from django.db import models
from clients.models import User, CartItems
# Create your models here.


class Address(models.Model):
    company = models.CharField(max_length=255, null=True)
    street = models.CharField(max_length=500, null=True)
    houseNumber = models.CharField(max_length=255, null=True)
    phonePrefix = models.CharField(max_length=20, null=True)
    phoneNumber = models.CharField(max_length=255, null=True)
    zipcode = models.CharField(max_length=20, null=True)
    city = models.CharField(max_length=100, null=True)
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name='address', null=True)


class OrderGroup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItems, related_name='items')
    delivery_address = models.ForeignKey(
        Address, null=True, on_delete=models.SET_NULL,
        related_name='delivery_address'
    )
    billing_address = models.ForeignKey(
        Address, null=True, on_delete=models.SET_NULL,
        related_name='billing_address'
    )

    order_placed = models.BooleanField(default=False)
