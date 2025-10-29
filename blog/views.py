# blog/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import BlogPost
from .serializers import BlogPostSerializer
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import logging
from .permisions import IsAuthenticatedOrReadOnly

logger = logging.getLogger('blog')

# Vista para listar y crear blogposts
@method_decorator(csrf_exempt, name='dispatch')
class BlogPostListCreate(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        
        blogposts = BlogPost.objects.all()
        serializer = BlogPostSerializer(blogposts, many=True)
        logger.info("Blogposts retrieved successfully!")
        return Response(serializer.data)

    def post(self, request):

        if not request.user or not request.user.is_authenticated:
            logger.warning("Unauthorized attempt to create a blogpost.")
            return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = BlogPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"Blogpost created successfully by user {request.user.username}.")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        logger.error(f"Blogpost creation failed: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# Vista para obtener, actualizar y eliminar un blogpost específico
@method_decorator(csrf_exempt, name='dispatch')
class BlogPostDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, post_id):
        try:
            return BlogPost.objects.get(id=post_id)
        except BlogPost.DoesNotExist:
            return None

    def get(self, request, post_id):

        blogpost = self.get_object(post_id)
        if not blogpost:
            logger.warning(f"Blogpost with id {post_id} not found.")
            return Response({'error: Blogpost not found'},status=status.HTTP_404_NOT_FOUND)
        serializer = BlogPostSerializer(blogpost)
        logger.info(f"Blogpost with id {post_id} retrieved successfully!")
        return Response(serializer.data)
    
    def put(self, request, post_id):

        if not request.user or not request.user.is_authenticated:
            logger.warning("Unauthorized attempt to update a blogpost.")
            return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
        
        blogpost = self.get_object(post_id)
        if not blogpost:
            logger.warning(f"Blogpost with id {post_id} not found for update.")
            return Response ({'error': 'Blogpost not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = BlogPostSerializer(blogpost, data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"Blogpost with id {post_id} updated successfully by user {request.user.username}.")
            return Response(serializer.data)
        
        logger.error(f"Blogpost update failed for id {post_id}: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, post_id):

        if not request.user or not request.user.is_authenticated:
            logger.warning("Unauthorized attempt to delete a blogpost.")
            return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)

        blogpost = self.get_object(post_id)
        if not blogpost:
            logger.warning(f"Blogpost with id {post_id} not found for deletion.")
            return Response({'error': 'Blogpost not found'}, status=status.HTTP_404_NOT_FOUND)
        
        blogpost.delete()
        logger.info(f"Blogpost with id {post_id} deleted successfully by user {request.user.username}.")
        return Response(status=status.HTTP_204_NO_CONTENT)