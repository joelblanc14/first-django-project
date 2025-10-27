from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_posts, name='list_posts'),
]