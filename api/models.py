from django.db import models

# Create your models here.

class ApiCache(models.Model):
    product = models.CharField(max_length=255)
    response = models.TextField(null=True)

