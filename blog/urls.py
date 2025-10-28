from django.urls import path
from .views import BlogPostListCreate, BlogPostDetail

urlpatterns = [
    path('blogpost/', BlogPostListCreate.as_view(), name='blogpost_list_create'),
    path('blogpost/<int:post_id>/', BlogPostDetail.as_view(), name='blogpost_detail'),
]