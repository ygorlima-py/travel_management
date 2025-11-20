from django.db import models
from django.conf import settings
from .state import State   
from .team import Team


class UserProfile(models.Model):
    ACCOUNT_CHOICES = [
        ('Conta corrente', 'Conta corrente'),
        ('Conta poupança', 'Conta poupança'),
        ('Conta salário', 'Conta salário'),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
        )
    
    phone = models.CharField(
                        max_length=15,
                        blank=True,
                        null=True
                        )
    
    state_uf = models.ForeignKey(
                    State,
                    on_delete=models.PROTECT,
                    blank=True, 
                    null=True,
                    )
    
    team = models.ForeignKey(
                Team,
                on_delete=models.SET_NULL,
                blank=True,
                null=True,
    )

    city = models.CharField(
                            max_length=50,
                            blank=True,
                            null=True,
                            )
    
    cost_center = models.CharField(
                        max_length=25,
                        blank=True,
                        null=True,
    )

    fleet_number = models.CharField(
                            max_length=20,
                            blank=True,
                            null=True,
                            )
    
    bank = models.CharField(
                max_length=50,
                blank=True,
                null=True,
    )

    agency = models.CharField(
                    max_length=10,
                    blank=True,
                    null=True,
    )

    account = models.CharField(
                    max_length=15,
                    blank=True,
                    null=True,
    )

    account_type = models.CharField(
                    max_length=15,
                    blank=True,
                    null=True,
                    choices=ACCOUNT_CHOICES,
                    default='',
    )

    
    def __str__(self):
        return f'Profile: {self.user.username}' # type:ignore