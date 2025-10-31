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
        
        # Usuarios normales solo pueden modificar sus propios objetos
        return hasattr(obj, 'autor') and obj.autor == request.user