from django.contrib import admin
from .models import Address, OrderGroup

admin.site.register(OrderGroup)
admin.site.register(Address)
