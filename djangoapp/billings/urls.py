from django.urls import path
from .views import CreateCheckoutSessionView, SuccessView, CancelView


urlpatterns = [
    path('checkout/<int:plan_id>/<str:cycle>/', CreateCheckoutSessionView.as_view(), name="billing_checkout"),
    path("success/", SuccessView.as_view(), name="billing_success"),
    path("cancel/", CancelView.as_view(), name="billing_cancel"),
]