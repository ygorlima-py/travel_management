from django.db import models
from django.conf import settings

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

    stripe_price_monthly_id = models.CharField(max_length=255, blank=True, null=True)
    
    stripe_price_yearly_id = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name # type: ignore
    
class UserSubscription(models.Model):
    STATUS_CHOICES = [
        ("inactive", "Inactive"),
        ("active", "Active"),
        ("trialing", "Trialing"),
        ("past_due", "Past due"),
        ("canceled", "Canceled"),
        ("incomplete", "Incomplete"),
        ("unpaid", "Unpaid"),
    ]
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, null=True, blank=True, on_delete=models.SET_NULL)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="inactive")
    current_period_end = models.DateTimeField(null=True, blank=True)

    stripe_customer_id = models.CharField(max_length=255, blank=True, null=True)
    stripe_subscription_id = models.CharField(max_length=255, null=True, blank=True)

    billing_cycle = models.CharField(
        max_length=10,
        choices=[("monthly", "Monthly"), ("yearly", "Yearly")],
        null=True,
        blank=True,
    )
    updated_at = models.DateTimeField(auto_now=True)



