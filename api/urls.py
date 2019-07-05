from django.urls import path
from .views import *

urlpatterns = [
    path('catalog/', catalog_api),
    path('create_product/', create_product),
    path('file_upload/', file_upload),
    path('test',create_session)
]
