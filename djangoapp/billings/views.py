import stripe
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from expenses.models import Plan

stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

class CreateCheckoutSessionView(LoginRequiredMixin, View):
    def post(self, request, plan_id, cycle):
        plan = Plan.objects.get(pk=plan_id) 
        price_id = plan.stripe_price_monthly_id if cycle == "monthly" else plan.stripe_price_yearly_id
        success_url = f"/user/profile/{request.user.username}/"

        session = stripe.checkout.Session.create(
            mode="subscription",
            line_items=[{"price": price_id, "quantity": 1}],
            success_url=request.build_absolute_uri(success_url),
            cancel_url=request.build_absolute_uri("/billing/cancel"),
            metadata={
                "user_id": str(request.user.id),
                "plan_id": str(plan.id),
                "billing_cycle": cycle,
            },
        )

        return JsonResponse({"url": session.url})
    

class SuccessView(View):
    def get(self, request):
        return HttpResponse("Pagamento concluído com sucesso, você pode voltar ao app")
    
class CancelView(View):
    def get(self, request):
        return HttpResponse("Pagamento cancelado")


