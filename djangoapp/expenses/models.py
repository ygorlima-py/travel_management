from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Category(models.Model):
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name

class Status(models.Model):
    class Meta:
        verbose_name = 'Status'
        verbose_name_plural = 'Status'
        
    name = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.name

class State(models.Model):
    class Meta:
        verbose_name = 'Estado'
        verbose_name_plural = 'Estados'
    
    name = models.CharField(
                    max_length=30,
                    unique=True,
                            )
    
    uf_name = models.CharField(
                    max_length=2,
                    unique=True
                )
    
    def __str__(self) -> str:
        return f'{self.name}-{self.uf_name}'

class Cycle(models.Model):
    class Meta:
        verbose_name = 'Ciclo'

    name = models.CharField(
                    max_length=40,
                    blank=False,
                    null=False,
                    )
    initial_date = models.DateField(
                blank=False,
                null=False, 
    )
    end_date = models.DateField(
                blank=False,
                null=False,
    )
    initial_km = models.IntegerField(
                blank=True,
                null=True,
    )
    end_km = models.IntegerField(
                blank=True,
                null=True,
    )
    is_open = models.BooleanField(
                    default=True,
    )
    save_expense_auto = models.BooleanField(
                blank=True,
                null=True,
                default=True
    )
    owner = models.ForeignKey(
            User,
            on_delete=models.PROTECT,
            related_name='cycles_owner'
    )

    def __str__(self) -> str:
        return self.name

class Expenses(models.Model):
    class Meta:
        verbose_name = 'Despesa'
        verbose_name_plural = 'Despesas'

    category = models.ForeignKey(
                            Category,
                            on_delete=models.PROTECT,
                            blank=False,
                            null=False, 
                            help_text='Selecione a cataegoria da despesa',                       
                            )
    
    supply = models.CharField(
                    max_length=150,
                    blank=True,
                    null=True, 
                    )
    
    state_uf = models.ForeignKey(
                    State,
                    on_delete=models.PROTECT,
                    blank=True, 
                    null=True,
                    )
    
    city = models.CharField(
                    max_length=150,
                    blank=True,
                    null=True, 
                    )
    
    nf = models.CharField(
                max_length=9,
                blank=True,
                null=True,
                )
    
    date = models.DateTimeField(
                        null=True,
                        blank=True
                        )
    
    amount = models.FloatField(
                        null=True,
                        blank=True,
                        help_text='Adicione a quantidade aqui',
                        )

    value = models.DecimalField(
                decimal_places=2,
                help_text='Digite o valor total da despesa',
                max_digits=10, 
                null=True, 
                blank=True,
                )
    
    description = models.TextField(
                help_text='Escreva a descriminação da despesa',
                blank=True,
            )
    
    picture = models.ImageField(
                blank=True, 
                upload_to='pictures/%Y/%m/',
                help_text='Adicione a imagem da nota fiscal')
    
    owner_expenses = models.ForeignKey(User, 
                                on_delete=models.SET_NULL,
                                blank=True,
                                null=True,
                                related_name='expenses_owner'
                                )
    
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    cycle = models.ForeignKey(
        Cycle,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name = 'expenses',
    )

    def save(self, *args, **kwargs):
        if not self.status:            
            self.status = Status.objects.get(name='PENDENTE')
        super().save(*args, **kwargs)
        
    def __str__(self) -> str:
        return self.supply # type: ignore

class UserProfile(models.Model):
    ACCOUNT_CHOICES = [
        ('Conta corrente', 'Conta corrente'),
        ('Conta poupança', 'Conta poupança'),
        ('Conta salário', 'Conta salário'),
    ]

    user = models.OneToOneField(
        User,
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

class AlertRecused(models.Model):
    class Meta:
        verbose_name = 'Alerta de Recusa'
        verbose_name_plural = 'Alertas de Recusa'

    message = models.CharField(
        max_length=40,
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    expense = models.ForeignKey(
        Expenses,
        on_delete=models.CASCADE,
        related_name='alerts_recused',
    )

    def __str__(self) -> str:
        return self.message # type: ignore
    
class Plan(models.Model):
    name = models.CharField(
                    max_length=255,
                    null=True,
                    blank=True,
    )

    price = models.DecimalField(
                decimal_places=2,
                max_digits=10,
                null=True,
    )

    description = models.TextField(blank=True)

    max_users = models.IntegerField(default=1)

    max_team = models.IntegerField(default=1)

    status = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name
    
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

class Roles(models.Model):
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
        return self.name
    
class Team(models.Model):
    name = models.CharField(
                    max_length=255,
                    null=False,
                    blank=False,
    )

    enterprise = models.ForeignKey(
                    EnterPrise,
                    on_delete=models.CASCADE,
                    related_name='teams',
    )

    team_manager = models.ForeignKey(
                    settings.AUTH_USER_MODEL,
                    on_delete=models.SET_NULL,
                    related_name='managed_teams',
                    null=True,
                    blank=True,
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

