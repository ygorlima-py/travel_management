from .mixin import PermissionMixin
from django.http import HttpResponseForbidden
from functools import wraps

def is_manager_or_company_admin(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):

        if PermissionMixin.is_company_admin(request.user) or PermissionMixin.is_manager(request.user):
            return func(request, *args, **kwargs)
        
        return HttpResponseForbidden("Not Permission")
    return wrapper


