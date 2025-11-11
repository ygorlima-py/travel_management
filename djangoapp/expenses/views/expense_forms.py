from django.shortcuts import render, redirect, get_object_or_404
from expenses.form import ExpenseForm
from expenses.models import Expenses
from django.urls import reverse
from django.contrib.auth.decorators import login_required


# @login_required(login_url='expense:login')
def create(request):
    form_action = reverse('expense:create')

    if request.method == 'POST':
        
        form = ExpenseForm(request.POST, request.FILES)
        
        context = dict(
            form=form,
            form_action=form_action,
        )

        print(context)

        if form.is_valid():        
            expense = form.save(commit=False) # Grarante que eu não salve na base de dados ainda
            expense.owner = request.user # Informo para expense.owner que esse contato pertence a esse usuário
            expense.save()
            return redirect('expense:create')

        return render(
        request,
        'expenses/pages/create_expense.html',
        context,
        )

    context = dict(
        form=ExpenseForm()
    )

    return render(
        request,
        'expenses/pages/create_expense.html',
        context, 
        )

