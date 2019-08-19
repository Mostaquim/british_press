from django.urls import path
from .views import *

urlpatterns = [
    path('spinner/', page_generator, name="spinner"),
    path('spinner/<int:page>/', page_generator, name="spinner"),
    path('create_batch/', create_batch, name="create_batch"),
    path('article/', article, name="article"),
    path('article/<int:pk>/', article_edit ),
    path('article/new/', article_new ),
    path('article/<int:pk>/delete/', article_delete ),
    path('batch/', batch, name='batch' ),
    path('batch/<int:pk>/', batch_view, name='batch' ),
    path('batch/<int:pk>/start/', batch_start, name='batch' ),
]
