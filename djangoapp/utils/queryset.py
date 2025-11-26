from django.db import models
from .mixin import PermissionMixin

class ExpenseQuerySet(models.QuerySet):
    def for_user(self, user):  
        if PermissionMixin.is_operator(user):
            return self.filter(owner_expenses=user)
        
        if PermissionMixin.is_manager(user):
            return self.filter(owner_expenses__profile__team=user.profile.team)
        
        if PermissionMixin.is_company_admin(user):
            return self.filter(owner_expenses__profile__team__enterprise=user.profile.team.enterprise)
        
        return self.none()