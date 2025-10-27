from django.urls import path
from . import views

urlpatterns = [
    path('api/blogpost/', views.blogposts_api, name='list_blogposts'),
    path('api/blogpost/<int:post_id>/', views.blogpost_detail_api, name='blogpost_detail'),
]