from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from expenses.models import Expenses
from utils.mixin import PermissionMixin
from utils.decorators import is_manager_or_company_admin

# Create your views here.
@login_required(login_url='expense:login')
@is_manager_or_company_admin
def filter_per_user(request, username):
    User = get_user_model()

    enterprise = PermissionMixin.get_user_enterprise(request.user)
    employee = get_object_or_404(User, username=username, profile__enterprise=enterprise)
    expenses = Expenses.objects.for_user(request.user).filter(owner_expenses=employee)

    paginator = Paginator(expenses, 25)  # Show 25 contacts per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'site_title': 'Despesas - ',
    }

    return render(
        request=request,
        template_name='expenses/pages/index.html',
        context=context,
    )