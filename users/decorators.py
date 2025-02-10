from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required

def allowed_roles(allowed_roles=[]):
    def decorator(view_func):
        @login_required
        def wrapper(request, *args, **kwargs):
            if request.user.groups.filter(name__in=allowed_roles).exists():
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponseForbidden("You do not have permission to access this page.")
        return wrapper
    return decorator
