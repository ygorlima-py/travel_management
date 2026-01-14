from django.db import models
from django.conf import settings
from .enterprise import EnterPrise, Role
import uuid
from datetime import timedelta
from django.utils import timezone

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

    cost_center = models.CharField(
                        max_length=25,
                        blank=True,
                        null=True,
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

class TeamInvite(models.Model):
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name='invites'
    )

    email = models.EmailField()
    
    token = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
    )

    invited_by = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            on_delete=models.SET_NULL,        
            null=True,
            blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    expires_at = models.DateTimeField()

    accepted = models.BooleanField(default=False)

    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    class Meta:
        unique_together = ['team', 'email']
        verbose_name = 'Team Invite'
        verbose_name_plural = 'Team Invites'
    
    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(days=7)
        super().save(*args, **kwargs)
    
    def is_valid(self):

        return not self.accepted and timezone.now() < self.expires_at
    
    def __str__(self) -> str:
        return f"{self.email} - {self.team.name}"