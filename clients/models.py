from django.contrib.auth.models import User
from django.db import models
import os
# Create your models here.


class Clients(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.CharField(max_length=255, null=True)
    salutation = models.CharField(max_length=5, null=True)
    phone_prefix = models.CharField(max_length=10, null=True)
    phone_number = models.CharField(max_length=20, null=True)
    zip_code = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=255, null=True)
    street = models.CharField(max_length=255, null=True)
    house_number = models.CharField(max_length=255, null=True)


class CartItems(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    slug = models.CharField(null=True, max_length=255)
    data_vals = models.TextField(null=True)
    data_name = models.TextField(null=True)
    price_net = models.FloatField(null=True)
    price_gross = models.FloatField(null=True)
    shipping_net = models.FloatField(null=True)
    shipping_gross = models.FloatField(null=True)
    date = models.DateTimeField(auto_now_add=True, null=True)


class UploadedFile(models.Model):
    """
    oldTODO FINE build the uploaded file model
    name -> uploaded file name
    saved_name -> saved name on disk
    """
    name = models.CharField(max_length=255, null=True)
    saved_name = models.CharField(max_length=255, null=True)
    saved_path = models.CharField(max_length=500, null=True)
    file_type = models.CharField(max_length=255, null=True)
    cart_item = models.ForeignKey(
        CartItems,
        on_delete=models.SET_NULL,
        related_name='files',
        null=True
    )

    date = models.DateTimeField(auto_now_add=True, null=True)

    def delete(self):
        try:
            os.remove(self.saved_path)
        except:
            pass
        super(UploadedFile, self).delete()
