from djstripe.event_handlers import djstripe_receiver
from djstripe.models import Event, Subscription as DjSubscription
from django.utils import timezone
from expenses.models import UserSubscription

@djstripe_receiver("checkout.session.completed")
def on_checkout_completed(sender, **kwargs):
    event: Event = kwargs["event"]

    session = event.data["object"]
    user_id = session["metadata"].get("user_id")
    plan_id = session["metadata"].get("plan_id")
    cycle = session["metadata"].get("billing_cycle")

    stripe_customer_id = session.get("customer")
    stripe_subscription_id = session.get("subscription")

    us, _ = UserSubscription.objects.get_or_create(user_id=user_id)
    us.plan_id = plan_id
    us.billing_cycle = cycle
    us.stripe_customer_id = stripe_customer_id
    us.stripe_subscription_id = stripe_subscription_id
    us.save()

    print(f"Plano salvo com sucesso {plan_id}, ciclo {cycle}")

@djstripe_receiver("invoice.paid")
def on_invoice_paid(sender,**kwargs):
    event: Event = kwargs["event"]
    invoice = event.data["object"]

    stripe_subscription_id = invoice.get("subscriprion")
    if not stripe_subscription_id:
        return
    
    us = UserSubscription.objects.filter(stripe_subscription_id=stripe_subscription_id).first()
    if not us:
        return
    
    sub = DjSubscription.objects.filter(id=stripe_subscription_id).first()
    if not sub:
        return
    
    us.status = "acrtive"
    us.current_period_end = sub.current_period_end
    us.save()

@djstripe_receiver("invoice.payment_failed")
def on_invoice_failed(sender,**kwargs):
    event: Event = kwargs["event"]
    invoice = event.data["object"]

    stripe_subscription_id = invoice.get("subscriprion")
    if not stripe_subscription_id:
        return
    
    us = UserSubscription.objects.filter(stripe_subscription_id=stripe_subscription_id).first()
    if not us:
        return
    
    us.status = "past_due"
    us.save()

@djstripe_receiver("customer.subscription.deleted")
def on_subscription_deleted(sender, **kwargs):
    event: Event = kwargs["event"]
    sub = event.data["object"]
    stripe_subscription_id = sub.get("id")

    us = UserSubscription.objects.filter(stripe_subscription_id=stripe_subscription_id).first()
    if not us:
        return
    
    us.status = "canceled"
    us.save()







