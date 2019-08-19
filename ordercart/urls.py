from django.urls import path
from .views import *


urlpatterns = [
    path('list/', order_list),
    path('delivery/',delivery_option),
    path('review/',review),
    path('checkout/',checkout),
    path('complete/',complete),
]