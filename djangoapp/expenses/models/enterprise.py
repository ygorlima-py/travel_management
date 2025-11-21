from django.db import models
from django.conf import settings
from .plan import Plan

class EnterPrise(models.Model):
    name = models.CharField(
                    max_length=255,
                    null=False,
                    blank=False,
    )

    cnpj = models.CharField(
                    max_length=18,
                    unique=True,
                    null=True,
                    blank=True,
    )

    owner = models.ForeignKey(
                            settings.AUTH_USER_MODEL,
                            on_delete=models.CASCADE,
                            related_name='enterprise'
                            )
    
    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    plan_type = models.ForeignKey(
                        Plan,
                        on_delete=models.SET_NULL,
                        null=True,
                        blank=True,
                        )
    
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name

class Role(models.Model):
    name = models.CharField(
                    max_length=100,
                    null=True,
                    blank=True,
    )

    description = models.TextField(blank=True)

    hierarchy = models.IntegerField(default=1)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name  #type: ignore
    

class UserEnterpriseRole(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='enterprise_roles',
    )

    enterprise = models.ForeignKey(
        EnterPrise,
        on_delete=models.SET_NULL,
        related_name='permissions',
        blank=True,
        null=True
    )

    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
    )

    def __str__(self) -> str:
        return f'{self.user}-{self.role.name}'


    
