from django.db import models
from django.conf import settings 
from .cycle import Cycle
from .state import State 
from utils.queryset import ExpenseQuerySet

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
    
class Expenses(models.Model):

    objects = ExpenseQuerySet.as_manager()
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
    
    owner_expenses = models.ForeignKey(
                                settings.AUTH_USER_MODEL, 
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