from utils.mixin import PermissionMixin
from django.contrib.auth.decorators import login_required

def system_info(request):
    manager = False
    operator = False

    if request.user.is_authenticated:
        manager = PermissionMixin.is_manager(request.user)
        operator = PermissionMixin.is_operator(request.user)

    return {
        'manager': manager,
        'operator': operator,
    }
