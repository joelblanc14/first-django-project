# blog/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from drf_spectacular.utils import extend_schema
import logging

from .models import BlogPost, Comentario
from .serializers import BlogPostSerializer, ComentarioSerializer
from .permisions import IsOwnerOrAdmin

logger = logging.getLogger('blog')


# -----------------------------
# BlogPost Views
# -----------------------------

class BlogPostListCreate(APIView):
    permission_classes = [IsOwnerOrAdmin]

    @extend_schema(request=BlogPostSerializer)
    def get(self, request):
        blogposts = BlogPost.objects.all().order_by('id')

        paginator = PageNumberPagination()
        paginator.page_size = 100
        paginated_blogposts = paginator.paginate_queryset(blogposts, request)

        serializer = BlogPostSerializer(paginated_blogposts, many=True)
        logger.info("Blogposts retrieved successfully!")
        return Response(serializer.data)

    @extend_schema(request=BlogPostSerializer)
    def post(self, request):
        if not request.user.is_authenticated:
            logger.warning("Unauthorized blogpost creation attempt.")
            return Response({"detail": "Authentication required"}, status=403)
        
        serializer = BlogPostSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # Asignar autor automáticamente
            serializer.save(autor=request.user)
            logger.info(f"Blogpost created successfully by user {request.user.username}.")
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        logger.error("Blogpost creation failed due to invalid data.")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BlogPostDetail(APIView):
    permission_classes = [IsOwnerOrAdmin]

    def get_object(self, post_id):
        try:
            return BlogPost.objects.get(id=post_id)
        except BlogPost.DoesNotExist:
            return None

    def get(self, request, post_id):
        blogpost = self.get_object(post_id)
        if not blogpost:
            logger.warning(f"Blogpost with id {post_id} not found.")
            return Response({'error': 'Blogpost not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = BlogPostSerializer(blogpost)
        logger.info(f"Blogpost with id {post_id} retrieved successfully!")
        return Response(serializer.data)

    @extend_schema(request=BlogPostSerializer)
    def put(self, request, post_id):
        blogpost = self.get_object(post_id)
        if not blogpost:
            logger.warning(f"Blogpost with id {post_id} not found for update.")
            return Response({'error': 'Blogpost not found'}, status=status.HTTP_404_NOT_FOUND)

        # Verifica permisos
        self.check_object_permissions(request, blogpost)

        serializer = BlogPostSerializer(blogpost, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        logger.info(f"Blogpost with id {post_id} updated successfully by user {request.user.username}.")
        return Response(serializer.data)

    def delete(self, request, post_id):
        blogpost = self.get_object(post_id)
        if not blogpost:
            logger.warning(f"Blogpost with id {post_id} not found for deletion.")
            return Response({'error': 'Blogpost not found'}, status=status.HTTP_404_NOT_FOUND)

        # Verifica permisos
        self.check_object_permissions(request, blogpost)

        blogpost.delete()
        logger.info(f"Blogpost with id {post_id} deleted successfully by user {request.user.username}.")
        return Response(status=status.HTTP_204_NO_CONTENT)


# -----------------------------
# Comentario Views
# -----------------------------

class ComentarioListCreate(APIView):
    permission_classes = [IsOwnerOrAdmin]

    def get(self, request, post_id):
        comentarios = Comentario.objects.filter(blog_post__id=post_id).order_by('fecha_creacion')
        serializer = ComentarioSerializer(comentarios, many=True)
        logger.info(f"Comments for blogpost id {post_id} retrieved successfully!")
        return Response(serializer.data)

    def post(self, request, post_id):

        if not request.user.is_authenticated:
            logger.warning("Unauthorized comment creation attempt.")
            return Response({"detail": "Authentication required"}, status=403)
        serializer = ComentarioSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Asignar autor
        serializer.save(blog_post_id=post_id, autor=request.user.username)
        logger.info(f"Comment created successfully for blogpost id {post_id} by user {request.user.username}.")
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ComentarioDetail(APIView):
    permission_classes = [IsOwnerOrAdmin]

    def get_object(self, comentario_id):
        try:
            return Comentario.objects.get(id=comentario_id)
        except Comentario.DoesNotExist:
            return None

    def get(self, request, post_id, comentario_id):
        comentario = self.get_object(comentario_id)
        if not comentario:
            logger.warning(f"Comentario with id {comentario_id} not found.")
            return Response({'error': 'Comentario not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ComentarioSerializer(comentario)
        logger.info(f"Comentario with id {comentario_id} retrieved successfully!")
        return Response(serializer.data)

    def put(self, request, post_id, comentario_id):
        comentario = self.get_object(comentario_id)
        if not comentario:
            logger.warning(f"Comentario with id {comentario_id} not found for update.")
            return Response({'error': 'Comentario not found'}, status=status.HTTP_404_NOT_FOUND)

        # Verifica permisos
        self.check_object_permissions(request, comentario)

        serializer = ComentarioSerializer(comentario, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        logger.info(f"Comentario with id {comentario_id} updated successfully by user {request.user.username}.")
        return Response(serializer.data)

    def delete(self, request, post_id, comentario_id):
        comentario = self.get_object(comentario_id)
        if not comentario:
            logger.warning(f"Comentario with id {comentario_id} not found for deletion.")
            return Response({'error': 'Comentario not found'}, status=status.HTTP_404_NOT_FOUND)

        # Verifica permisos
        self.check_object_permissions(request, comentario)

        comentario.delete()
        logger.info(f"Comentario with id {comentario_id} deleted successfully by user {request.user.username}.")
        return Response(status=status.HTTP_204_NO_CONTENT)
