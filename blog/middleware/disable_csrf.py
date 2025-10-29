from django.utils.deprecation import MiddlewareMixin

class DeactivateCSRFMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Desactiva CSRF solo para rutas que empiezan por /api/
        if request.path.startswith('/api/'):
            setattr(request, '_dont_enforce_csrf_checks', True)