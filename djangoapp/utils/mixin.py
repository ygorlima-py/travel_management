
class PermissionMixin:
    """
    Helper class to verify user permissions.
    Use: Inherit in views or use static methods
    """  

    @staticmethod
    def is_company_admin(user):
        """Verify if user is COMPANY_ADMIN"""
        from expenses.models import UserEnterpriseRole
        return UserEnterpriseRole.objects.filter(
            user=user,
            role__name='COMPANY_ADMIN',
        ).exists()
    
    @staticmethod
    def is_manager(user):
        """Verify if user is MANAGER"""
        from expenses.models import UserEnterpriseRole
        return UserEnterpriseRole.objects.filter(
            user=user,
            role__name='MANAGER',
        ).exists()
    
    @staticmethod
    def is_operator(user):
        """Verify if user is OPERATOR"""
        from expenses.models import UserEnterpriseRole
        return UserEnterpriseRole.objects.filter(
            user=user,
            role__name='OPERATOR',
        ).exists()

    @staticmethod
    def get_user_team(user):
        """Return team of the user or None"""
        if hasattr(user, 'profile') and user.profile.team:
            return user.profile.team
        return None
    
    @staticmethod
    def get_user_enterprise(user):
        """Return enterprise of the user or None"""
        if hasattr(user, 'profile') and user.profile.enterprise:
            return user.profile.enterprise
        return None
    
    @staticmethod
    def get_user_role(user):
        """Return role name of the user or None"""
        from expenses.models import UserEnterpriseRole
        user_role = UserEnterpriseRole.objects.filter(user=user).first()
        if user_role:
            return user_role.role.name
        return None

    @staticmethod
    def can_view_expense(user, expense) -> bool:
        """
        Verify if user can see expense
        Rules:
        - COMPANY_ADMIN -> Can see All expenses from same enterprise
        - MANAGER -> Can see team expenses (same team)
        - OPERATOR -> Can see Only own expenses  
        - Owner -> Can see own expense
        """

        # Rule 1 is the owner
        if expense.owner_expenses == user:
            return True
        
        # Rule 2: Is COMPANY_ADMIN from same enterprise
        if PermissionMixin.is_company_admin(user):
            user_enterprise = PermissionMixin.get_user_enterprise(user)
            owner_enterprise = PermissionMixin.get_user_enterprise(expense.owner_expenses)
            if user_enterprise and user_enterprise == owner_enterprise:
                return True
        
        # Rule 3: Is Manager from same team    
        if PermissionMixin.is_manager(user):
            user_team = PermissionMixin.get_user_team(user)
            owner_team = PermissionMixin.get_user_team(expense.owner_expenses)
            if user_team and user_team == owner_team:
                return True
        
        # Rule 4: No permission
        return False
            
    @staticmethod
    def can_approve_expense(user, expense) -> bool:
        """
        Verify if user can see cycle
        
        Rules:
        1. CANNOT approve own expense
        2. COMPANY_ADMIN → Can approve ALL from same enterprise
        3. MANAGER → Can approve only team expenses (NOT own)
        4. OPERATOR → CANNOT approve
        """

        # Rule 1 is the owner
        if expense.owner_expenses == user:
            return False # Can not aprove expenses

        # Rule 2: COMPANY_ADMIN from same enterprise
        if PermissionMixin.is_company_admin(user):
            user_enterprise = PermissionMixin.get_user_enterprise(user)
            owner_enterprise= PermissionMixin.get_user_enterprise(expense.owner_expenses)
            if user_enterprise and user_enterprise == owner_enterprise:
                return True        
            
        # Rule 3: MANAGER from same Team
        if PermissionMixin.is_manager(user):
            user_team = PermissionMixin.get_user_team(user)
            owner_team = PermissionMixin.get_user_team(expense.owner_expenses)
            if user_team and user_team == owner_team:
                return True
            
        # Rule 4: No permission
        return False
    
    @staticmethod
    def can_manage_team(user, team) -> bool:
        """
        Verify if user can manage team (invite members, edit, etc)

        Rules:
        1. COMPANY_ADMIN -> Can manage ALL teams from enterprise
        2. MANAGER -> Can manage ONLY if is team_manager
        3. OPERATOR -> CANOT manage
        """

        # Rule 1: Is team manager
        if team.team_manager == user:
            return True
        
        if PermissionMixin.is_company_admin(user):
            user_enterprise = PermissionMixin.get_user_enterprise(user)
            if user_enterprise and user_enterprise == team.enterprise:
                return True
            
        return False
    
    @staticmethod
    def can_view_cycle(user, cycle) -> bool:
        """
        Verify if user can see cycle

        Rules:
        1. COMPANY_ADMIN -> Can see ALL cycles from enterprise
        2. MANAGER -> Can see cycles from team 
        3. OPERATOR -> Can see cycles if member of team
        """
        # Rule 1: COMPANY_ADMIN from same enterprise
        if PermissionMixin.is_company_admin(user):
            user_enterprise = PermissionMixin.get_user_enterprise(user)
            if user_enterprise and user_enterprise == cycle.enterprise:
                return True
            
        # Rule 2: MANAGER or OPERATOR from same team
        user_team = PermissionMixin.get_user_team(user)
        if user_team and user_team == cycle.team:
            return True
        
        return False
    
    @staticmethod
    def can_exclude_team(user, team) -> bool:

        # Only the company owner can delete teams.
        return team.enterprise.owner == user
    
    @staticmethod
    def can_invite_or_remove_member(user, team) -> bool:
        if not PermissionMixin.is_operator(user):
            user_enterprise = PermissionMixin.get_user_enterprise(user)
            
            if team.enterprise == user_enterprise:
                return True
            return False
        return False    

        
# Posso enviar convite?
# preciso ser manager da equipe ou company_admin
# a equipe precisa ser da minha empresa



