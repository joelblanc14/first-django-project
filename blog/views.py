import json
from .models import BlogPost
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@csrf_exempt
def blogposts_api(request):
    if request.method == 'GET':
        # Devolver todos los posts
        blog_posts = BlogPost.objects.all().values('id', 'titulo', 'contenido', 'fecha_creacion')
        return JsonResponse(list(blog_posts), safe=False)
    elif request.method == 'POST':
        # Crear un nuevo post desde JSON
        data = json.loads(request.body) # Leer JSON
        post = BlogPost.objects.create(
            titulo=data.get('titulo', ''),
            contenido=data.get('contenido', '')
        )

        return JsonResponse({
            'id': post.id,
            'titulo': post.titulo,
            'contenido': post.contenido,
            'fecha_creacion': post.fecha_creacion
        }, status=201)

@csrf_exempt
def blogpost_detail_api(request, post_id):
    try:
        blog_post = BlogPost.objects.get(id=post_id)
    except BlogPost.DoesNotExist:
        return JsonResponse({'error': 'Post not found'}, status=404)

    if request.method == 'GET':
        # Devolver un post específico
        return JsonResponse({
            'id': blog_post.id,
            'titulo': blog_post.titulo,
            'contenido': blog_post.contenido,
            'fecha_creacion': blog_post.fecha_creacion
        })
    elif request.method == 'PUT':
        # Actualizar un post existente desde JSON
        data = json.loads(request.body) # Leer JSON
        blog_post.titulo = data.get('titulo', blog_post.titulo)
        blog_post.contenido = data.get('contenido', blog_post.contenido)
        blog_post.save()

        return JsonResponse({
            'id': blog_post.id,
            'titulo': blog_post.titulo,
            'contenido': blog_post.contenido,
            'fecha_creacion': blog_post.fecha_creacion
        })
    elif request.method == 'DELETE':
        # Eliminar un post
        blog_post.delete()
        return JsonResponse({'message': 'Post deleted'}, status=204)