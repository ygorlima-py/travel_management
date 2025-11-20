from django.db import models
from django.conf import settings
from .enterprise import EnterPrise

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

