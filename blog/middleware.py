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
        # Saltar autenticación para rutas públicas
        if (
            request.path.startswith('/admin/') or
            request.path.startswith('/api/token/')
        ):
            return self.get_response(request)
        
        return self.get_response(request)