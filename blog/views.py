from django.shortcuts import render
from .models import Post
from django.http import JsonResponse

# Create your views here.
def list_posts(request):
    posts = list(Post.objects.values())
    return JsonResponse(posts, safe=False)