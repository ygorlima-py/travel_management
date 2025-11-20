from django.db import models

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