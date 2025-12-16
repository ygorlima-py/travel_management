from utils.mixin import PermissionMixin
from django.contrib.auth.decorators import login_required

def system_info(request):
    manager = False
    operator = False
    company_admin = False
    
    if request.user.is_authenticated:
        company_admin = PermissionMixin.is_company_admin(request.user)
        manager = PermissionMixin.is_manager(request.user)
        operator = PermissionMixin.is_operator(request.user)

    return {
        'company_admin': company_admin,
        'manager': manager,
        'operator': operator,
    }
