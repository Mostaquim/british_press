from django.contrib import admin
from .models import Clients, CartItems, UploadedFile
# Register your models here.
admin.site.register(Clients)
admin.site.register(CartItems)
admin.site.register(UploadedFile)
