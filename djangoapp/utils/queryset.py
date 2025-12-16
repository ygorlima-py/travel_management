from django.db import models
from .mixin import PermissionMixin

class ExpenseQuerySet(models.QuerySet):
    def for_user(self, user):  
        team = PermissionMixin.get_user_team(user)
        enterprise = PermissionMixin.get_user_enterprise(user)

        if PermissionMixin.is_operator(user):
            return self.filter(owner_expenses=user)
        
        if PermissionMixin.is_manager(user) and team:
            return self.filter(owner_expenses__profile__team=team)
        
        if PermissionMixin.is_company_admin(user) and enterprise:
            return self.filter(owner_expenses__profile__enterprise=enterprise)
        
        return self.none()
    
class CycleQuerySet(models.QuerySet):
    def for_user(self, user):  
        team = PermissionMixin.get_user_team(user)
        enterprise = PermissionMixin.get_user_enterprise(user)

        print('Essa é a desgraça da minha empresa: ', enterprise)

        if PermissionMixin.is_operator(user):
            return self.filter(owner=user)

        if PermissionMixin.is_manager(user) and team:
            return self.filter(owner__profile__team=team)

        if PermissionMixin.is_company_admin(user) and enterprise:
            return self.filter(owner__profile__enterprise=enterprise)
        
        return self.none()
    
