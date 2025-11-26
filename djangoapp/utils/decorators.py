from functools import wraps
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from expenses.models import UserEnterpriseRole

# Allows access if the user has a specific role.
def require_role(role_name):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            user_role = UserEnterpriseRole.objects.filter(
                user=request.user,
                role__name=role_name,
            ).first()

            if not user_role:
                messages.error(request,"Você não tem permissão")
                return redirect('expense:index')
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

# Allows access if the user is owner object expense or user is manager same team
def require_own_or_manager(model, pk_param='pk', owner_field='owner_expenses'):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):

            obj_id = kwargs.get(pk_param)
            obj = get_object_or_404(model, pk=obj_id)

            owner = getattr(obj, owner_field)

            if owner == request.user:
                return view_func(request, *args, **kwargs)

            is_manager = UserEnterpriseRole.objects.filter(
                user=request.user,
                role__name='MANAGER'
            ).exists()

            if is_manager and hasattr(request.user, "profile") and hasattr(owner, 'profile'):
                same_team = request.user.profile.team == owner.profile.team
                if same_team:
                    return view_func(request, *args, **kwargs)
                
            messages.error(request, "Você não tem permissão para este recurso")
        
        return wrapper
    return decorator