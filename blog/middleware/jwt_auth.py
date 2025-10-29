# blog/middleware.py
import jwt
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth.models import User
from http import HTTPStatus
import logging

logger = logging.getLogger('blog')

class SimpleAuthMiddleware:
    """
    Middleware personalizado para autenticar usuarios mediante un token JWT
    sin depender de rest_framework_jwt.
    """
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Saltar autenticación para rutas públicas
        if (
            request.path.startswith('/admin/') or
            request.path.startswith('/api/token/')
        ):
            logger.info(f"Public route accessed: {request.path}")
            return self.get_response(request)
        
        auth_header = request.headers.get('Authorization')

        if not auth_header or not auth_header.startswith('Bearer'):
            logger.warning("Authorization header missing or invalid")
            request.user = None
            return self.get_response(request)
        
        token = auth_header.split(' ')[1]
        
        try:
            # Decodificar el token JWT
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload.get('user_id')
            user = User.objects.get(id=user_id)
            request.user = user
            logger.info(f"User {user.username} authenticated successfully via JWT.")
        except jwt.ExpiredSignatureError:
            logger.warning("JWT token has expired")
            return JsonResponse({'error': 'El Token ha expirado'}, status=HTTPStatus.UNAUTHORIZED)
        except jwt.InvalidTokenError:
            logger.warning("Invalid JWT token")
            return JsonResponse({'error': 'Token inválido'}, status=HTTPStatus.UNAUTHORIZED)
        except User.DoesNotExist:
            logger.warning("User not found for given JWT token")
            return JsonResponse({'error': 'Usuario no encontrado'}, status=HTTPStatus.UNAUTHORIZED)
        except Exception as e:
            logger.error(f"Error during JWT authentication: {str(e)}")
            return JsonResponse({'error': str(e)}, status=HTTPStatus.UNAUTHORIZED)
        
        return self.get_response(request)