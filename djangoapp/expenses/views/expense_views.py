from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.db.models import Q
from django.core.paginator import Paginator
from expenses.models import Expenses, Category

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
    
    if single_expense is None:
        raise Http404()
    
    context = {
        'expense': single_expense,
    }

    return render (
        request=request,
        template_name='expenses/pages/expense.html',
        context=context,
    )


def expense_approved(request, expense_id):

    # Source - https://stackoverflow.com/a
    # Posted by Platinum Azure, modified by community. See post 'Timeline' for change history
    # Retrieved 2025-11-13, License - CC BY-SA 4.0
    obj, created = Expenses.objects.update_or_create(
        pk=expense_id,
        defaults={'status_id': 5},
    )

    if obj is None:
        raise Http404()
    
    if created == False:
        return redirect("expense:index")
    
def expense_recused(request, expense_id):

    # Source - https://stackoverflow.com/a
    # Posted by Platinum Azure, modified by community. See post 'Timeline' for change history
    # Retrieved 2025-11-13, License - CC BY-SA 4.0
    obj, created = Expenses.objects.update_or_create(
        pk=expense_id,
        defaults={'status_id': 6},
    )

    if obj is None:
        raise Http404()
    
    if created == False:
        return redirect("expense:index")


def categories(request):
    categories = Category.objects.order_by('-id')
    
    if categories is None:
        raise Http404()
    
    context = {
        'categories': categories,
    }

    return render (
        request=request,
        template_name='expenses/pages/categories.html',
        context=context,
    )
