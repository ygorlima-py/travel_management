from django.shortcuts import render, get_object_or_404, redirect
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
    print(f'SESSION: {request.session.items()}')
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
    
@login_required(login_url='expense:login')
def search(request):
    search_value = request.GET.get('q', '').strip()

    if search_value == '':
        return redirect('expense:index')

    expenses = Expenses.objects.for_user(request.user)
    page_obj = (
                expenses
                .filter(
                    Q(supply__icontains=search_value) |
                    Q(city__icontains=search_value) |
                    Q(nf__icontains=search_value) |
                    Q(category__name__icontains=search_value) |
                    Q(owner_expenses__first_name__icontains=search_value)
                )
                .order_by('-id')
            )
    
    paginator = Paginator(page_obj, 25)  # Show 25 contacts per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = dict(
        page_obj=page_obj,
        site_title='Search - '
    )
    return render(
        request,
        'expenses/pages/index.html',
        context,
    )