from django.db import models

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
        return self.name # type: ignore
    