from django.urls import path
from .views import BlogPostListCreate, BlogPostDetail, ComentarioListCreate, ComentarioDetail

urlpatterns = [
    path('blogpost/', BlogPostListCreate.as_view(), name='blogpost_list_create'),
    path('blogpost/<int:post_id>/', BlogPostDetail.as_view(), name='blogpost_detail'),
    path('blogpost/<int:post_id>/comentario/', ComentarioListCreate.as_view(), name='comentario_list_create'), 
    path('blogpost/<int:post_id>/comentario/<int:comentario_id>/', ComentarioDetail.as_view(), name='comentario_detail'),
]