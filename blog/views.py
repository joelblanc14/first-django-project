# blog/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import BlogPost
from .serializers import BlogPostSerializer

# Vista para listar y crear blogposts

class BlogPostListCreate(APIView):

    def get(self, request):
        
        blogposts = BlogPost.objects.all()
        serializer = BlogPostSerializer(blogposts, many=True)
        return Response(serializer.data)

    def post(self, request):

        if not request.user or not request.user.is_authenticated:
            return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = BlogPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# Vista para obtener, actualizar y eliminar un blogpost específico
# @method_decorator(csrf_exempt, name='dispatch')
class BlogPostDetail(APIView):

    def get_object(self, post_id):
        try:
            return BlogPost.objects.get(id=post_id)
        except BlogPost.DoesNotExist:
            return None

    def get(self, request, post_id):

        blogpost = self.get_object(post_id)
        if not blogpost:
            return Response({'error: Blogpost not found'},status=status.HTTP_404_NOT_FOUND)
        serializer = BlogPostSerializer(blogpost)
        return Response(serializer.data)
    
    def put(self, request, post_id):

        if not request.user or not request.user.is_authenticated:
            return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
        
        blogpost = self.get_object(post_id)
        if not blogpost:
            return Response ({'error': 'Blogpost not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = BlogPostSerializer(blogpost, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, post_id):

        if not request.user or not request.user.is_authenticated:
            return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)

        blogpost = self.get_object(post_id)
        if not blogpost:
            return Response({'error': 'Blogpost not found'}, status=status.HTTP_404_NOT_FOUND)
        blogpost.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)