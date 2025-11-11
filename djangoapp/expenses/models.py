from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=50)

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
    

    
    def __str__(self) -> str:
        return self.supply # type: ignore

class UserProfile(models.Model):
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
    fleet_number = models.CharField(
                            max_length=20,
                            blank=True,
                            null=True,
                            )
    
    def __str__(self):
        return f'Profile: {self.user.username}'
