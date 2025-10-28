# blog/middleware.py
from django.http import JsonResponse
from django.contrib.auth.models import User
from http import HTTPStatus

class SimpleAuthMiddleware:
    """
    Middleware simple para autenticar usuarios 
    basados en un token en el header
    """
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Saltarse autenticación para admin
        if request.path.startswith('/admin/'):
            return self.get_response(request)
        
        # 1. Obtener el token del header
        token = request.headers.get('Authorization')

        if not token:
            return JsonResponse({'error': 'Falta el token'}, status=HTTPStatus.UNAUTHORIZED)
        
        # Validar el token
        try:
            user = User.objects.get(auth_token__key=token)
            request.is_authenticated = True
            request.user = user
            request._user = user
        except User.DoesNotExist:
            return JsonResponse({'error': 'Token inválido'}, status=HTTPStatus.UNAUTHORIZED)
        
        # 3. Dejar pasar la request
        response = self.get_response(request)
        return response