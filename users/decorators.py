from django.http import HttpResponseForbidden
from functools import wraps
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

def allowed_roles(roles=[]):
    def decorator(view_func):
        @wraps(view_func)
        @login_required  
        def wrapper_func(request, *args, **kwargs):
            if request.user.is_authenticated:
                if request.user.groups.filter(name__in=roles).exists():
                    return view_func(request, *args, **kwargs)
                else:
                    raise PermissionDenied  
            return HttpResponseForbidden("You must be logged in to access this page.")
        return wrapper_func
    return decorator
