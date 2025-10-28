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
        
        # Obtener el token del header (Bearer token)
        auth_header = request.headers.get('Authorization')
        if auth_header:
            parts = auth_header.split()
            if len(parts) == 2 and parts[0].lower() == 'bearer':
                token = parts[1]
            else: 
                return JsonResponse({'error': 'Formato de token inválido'}, status=HTTPStatus.UNAUTHORIZED)
        else:
            return JsonResponse({'error': 'Token no proporcionado'}, status=HTTPStatus.UNAUTHORIZED)
        
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