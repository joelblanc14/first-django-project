import json
from .models import BlogPost
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

# Función para serializar un blogpost
def serialize_blogpost(post):
    return {
        'id': post.id,
        'titulo': post.titulo,
        'contenido': post.contenido,
        'fecha_creacion': post.fecha_creacion,
    }

# Funcion para validar datos de entrada
def validate_blogpost_data(data):
    errors = {}
    if 'titulo' not in data or not data['titulo'].strip():
        errors['titulo'] = 'El título es obligatorio.'
    if 'contenido' not in data or not data['contenido'].strip():
        errors['contenido'] = 'El contenido es obligatorio.'
    return errors

@csrf_exempt
def blogposts_api(request):
    if request.method == 'GET':
        # Devolver todos los posts
        blog_posts = BlogPost.objects.all()
        data = [serialize_blogpost(post) for post in blog_posts]
        return JsonResponse(data, safe=False)
    
    elif request.method == 'POST':
        # Crear un nuevo post desde 
        try:
            data = json.loads(request.body) # Leer JSON
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        
        errors = validate_blogpost_data(data)
        if errors:
            return JsonResponse({'errors': errors}, status=400)
        
        post = BlogPost.objects.create(
            titulo=data.get('titulo', ''),
            contenido=data.get('contenido', '')
        )

        return JsonResponse(serialize_blogpost(post), status=201)

@csrf_exempt
def blogpost_detail_api(request, post_id):
    try:
        blog_post = BlogPost.objects.get(id=post_id)
    except BlogPost.DoesNotExist:
        return JsonResponse({'error': 'Post not found'}, status=404)

    if request.method == 'GET':
        # Devolver un post específico
        return JsonResponse(serialize_blogpost(blog_post))
    
    elif request.method == 'PUT':
        try:
            # Actualizar un post existente desde JSON
            data = json.loads(request.body) # Leer JSON
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        
        errors = validate_blogpost_data(data)
        if errors:
            return JsonResponse({'errors': errors}, status=400)
        
        blog_post.titulo = data.get('titulo', blog_post.titulo)
        blog_post.contenido = data.get('contenido', blog_post.contenido)
        blog_post.save()

        return JsonResponse(serialize_blogpost(blog_post))
    
    elif request.method == 'DELETE':
        # Eliminar un post
        blog_post.delete()
        return JsonResponse({'message': 'Post deleted'}, status=204)