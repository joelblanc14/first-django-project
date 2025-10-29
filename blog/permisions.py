# blog/permisions.py
from rest_framework.permissions import BasePermission
import logging

logger = logging.getLogger('blog')

class IsAuthenticatedOrReadOnly(BasePermission):
    """
    Permite GET a usuarios autenticados
    Permite todo (GET, POST, PUT, DELETE) solo a superusuarios
    """

    def has_permission(self, request, view):
        user = request.user

        # Superusuario puede hacer todo
        if user and user.is_superuser:
            logger.info(f"Access granted: Superuser: {user.username}, Method: {request.method}, Path: {request.path}")
            return True
        
        # Usuarios autenticados solo GET
        if request.method == 'GET' and user and user.is_authenticated:
            logger.info(f"Access granted: User: {user.username}, Method: {request.method}, Path: {request.path}")
            return True
        
        # Los demás casos -> acceso denegado
        logger.warning(f"Permission denied: User: {user}, Method: {request.method}, Path: {request.path}")
        return False
