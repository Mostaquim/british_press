from django.urls import path
from .views import *

urlpatterns = [
    path('catalog/', catalog_api),
    path('add_to_cart/', add_to_cart),
    path('file_upload/', file_upload),
    path('remove_cart/',remove_item_from_cart),
    path('upload_design/', upload_design),
    path('remove_file/', delete_file),
    path('create_address/', create_address),
    path('select_address/', select_address),
]
