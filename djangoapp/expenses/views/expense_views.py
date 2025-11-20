from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.db.models import Q
from django.core.paginator import Paginator
from expenses.models import Expenses

# Create your views here.

@login_required(login_url='expense:login')
def index(request):
    expenses = Expenses.objects.order_by('-id')
    paginator = Paginator(expenses, 25)  # Show 25 contacts per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'site_title': 'Despesas - '
    }

    return render(
        request=request,
        template_name='expenses/pages/index.html',
        context=context,
    )

@login_required(login_url='expense:login')
def expense(request, expense_id):
    single_expense = Expenses.objects.filter(pk=expense_id).first()
    last_alert = single_expense.alerts_recused.last() # Pega o ultimo alerta # type:ignore
    
    if single_expense is None:
        raise Http404()
    
    context = {
        'expense': single_expense,
        'alert': last_alert,
    }

    return render (
        request=request,
        template_name='expenses/pages/expense.html',
        context=context,
    )
    
@login_required(login_url='expense:login')
def dashbords(request):

    context = dict(
        is_dashbord=True,
    )

    return render (
        request=request,
        template_name='expenses/pages/dashbords.html',
        context=context
    )