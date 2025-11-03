from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone

# Manager 
class BlogPostManager(models.Manager):
    # Obtener posts publicados los últimos 7 días
    def recent_posts(self):
        una_semana_atras = timezone.now() - timedelta(days=7)
        return self.filter(fecha_creacion__gte=una_semana_atras)
    
    def get_by_author(self, author_username):
        return self.filter(autor__username=author_username)

# Create your models here.
class BlogPost(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blogposts')

    objects = BlogPostManager()

    def __str__(self):
        return self.titulo
    
class Comentario(models.Model):
    blog_post = models.ForeignKey(BlogPost, related_name='comentarios', on_delete=models.CASCADE)
    autor = models.CharField(max_length=100)
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comentario de {self.autor} en {self.blog_post.titulo}'