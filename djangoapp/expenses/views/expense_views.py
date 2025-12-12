from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.db.models import Q
from django.core.paginator import Paginator
from expenses.models import Expenses
from utils.mixin import PermissionMixin

# Create your views here.
@login_required(login_url='expense:login')
def index(request):
    expenses = Expenses.objects.for_user(request.user)
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

@login_required(login_url='expense:login')
def expense(request, expense_id):
    single_expense = get_object_or_404(Expenses.objects.for_user(request.user), pk=expense_id)
    last_alert = single_expense.alerts_recused.last() # Pega o ultimo alerta # type:ignore
    role = PermissionMixin.get_user_role(request.user)
    
    context = {
        'expense': single_expense,
        'alert': last_alert,
        'role': role,
    }

    return render (
        request=request,
        template_name='expenses/pages/expense.html',
        context=context,
    )
    
@login_required(login_url='expense:login')
def dashbords(request):
    
    if PermissionMixin.is_company_admin(request.user):

        context = dict(
            is_dashbord=True,
        )
        return render (
            request=request,
            template_name='expenses/pages/dashbords_admin.html',
            context=context,
        )
    
    elif PermissionMixin.is_manager(request.user):
        context = dict(
            is_dashbord=True,
        )
        return render (
            request=request,
            template_name='expenses/pages/dashbords_manager.html',
            context=context,
        )
    elif PermissionMixin.is_operator(request.user):
        context = dict(
            is_dashbord=True,
        )
        return render (
            request=request,
            template_name='expenses/pages/dashbords_operator.html',
            context=context,
        )