from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrAdmin(BasePermission):
    """
    Permiso que permite a superusuarios hacer cualquier cosa,
    y a usuarios normales solo sobre sus propios objetos.
    """

    def has_object_permission(self, request, view, obj):
        # Métodos seguros (GET, HEAD, OPTIONS) están permitidos para todos
        if request.method in SAFE_METHODS:
            return True
        # Superusuario puede hacer cualquier cosa
        if request.user.is_superuser:
            return True
        # Para BlogPost: autor es un User
        if hasattr(obj, 'autor') and hasattr(obj.autor, 'id'):
            return obj.autor == request.user
        # Para Comentario: autor es un string (username)
        if hasattr(obj, 'autor') and isinstance(obj.autor, str):
            return obj.autor == request.user.username
        return False