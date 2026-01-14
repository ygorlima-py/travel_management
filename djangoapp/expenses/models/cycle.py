from django.db import models
from django.conf import settings
from utils.queryset import CycleQuerySet

class Cycle(models.Model):

    objects = CycleQuerySet.as_manager()

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
                default=True,
    )
    owner = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            on_delete=models.PROTECT,
            related_name='owned_cicles',
    )

    def __str__(self) -> str:
        return self.name