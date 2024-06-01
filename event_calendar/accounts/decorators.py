# accounts/decorators.py

from django.core.exceptions import PermissionDenied

def staff_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied("Você não tem permissão para acessar esta página.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view
