from django.shortcuts import render, redirect, get_object_or_404
from expenses.form import ExpenseForm, AlertRecusedForm
from expenses.models import Expenses
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from utils.conditions import Conditions #type: ignore
from django.http import Http404
from utils.mixin import PermissionMixin

@login_required(login_url='expense:login')
def create_expense(request):
    form_action = reverse('expense:create')

    if request.method == 'POST':        
        form = ExpenseForm(request.POST, request.FILES)        
        context = dict(
            form=form,
            form_action=form_action,
        )

        if form.is_valid():        
            expense = form.save(commit=False) # Grarante que eu não salve na base de dados ainda
            expense.owner_expenses = request.user # Informo para expense.owner que esse contato pertence a esse usuário
            condition = Conditions(expense)
            cycle_id = condition.verify()

            if cycle_id is not None:
                expense.cycle_id = cycle_id
                
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

@login_required(login_url='expense:login')
def expense_update(request, expense_id):
    expense = get_object_or_404(Expenses, pk=expense_id)
    
    if request.method == "POST":
        form = ExpenseForm(request.POST, request.FILES, instance=expense)
        if form.is_valid():
            updated_expense = form.save(commit=False)
            updated_expense.owner_expenses = request.user

            condition = Conditions(expense)
            cycle_id = condition.verify()
            if cycle_id is not None:
                updated_expense.cycle_id = cycle_id

            updated_expense.save()

            expense.status_id = 4 #type: ignore
            expense.save(update_fields=['status_id'])
            
            messages.success(request, "Despesa atualizada")
            return redirect('expense:index')
        
    else:
        form = ExpenseForm(instance=expense)
    
    context = {
        'form': form,
        'expense':expense,
        'is_expense_update': True,
    }

    return render(
        request,
        'expenses/pages/create_expense.html',
        context,      
    )

@login_required(login_url='expense:login')
def expense_delete(request, expense_id):
    # 1) Busca o contato pelo id; se não existir (ou show=False), retorna 404
    expense = get_object_or_404(Expenses, pk=expense_id, owner_expenses=request.user)

    print('Despesa', expense)

    confirmation = request.POST.get('confirmation', 'no')
    print('confirmation', confirmation)


    if confirmation == 'yes':
        expense.delete()
        return redirect('expense:index')

    return render(
        request,
        'expenses/pages/expense.html',
        {
            'expense': expense,
            'confirmation': confirmation,
            'user': expense.owner_expenses,
        }
    )

@login_required(login_url='expense:login') #type:ignore
def expense_approved(request, expense_id):
    expense = get_object_or_404(Expenses, pk=expense_id)

    # Validation 1: Can not approve own expenses
    if expense.owner_expenses == request.user:
        messages.error(request, 'Você não pode aprovar as próprias despesas')
        return redirect('expense:expense', expense_id=expense_id)
    
    # Validation 2: Is need be of same team
    if not PermissionMixin.can_approve_expense(request.user, expense):
        messages.error(request, "Você não pode aprovar despesas de outra equipe")
        return redirect("expenses:index")
    
    # Validation 3: The expense status must be pending
    if expense.status_id != 4:
        messages.error(request, 'Só é possível aprovar despesas pendentes')
        return redirect("expense:expense", expense_id=expense_id)
    
    # Approve
    expense.status_id = 5
    expense.save(update_fields=['status_id'])

    messages.success(request, f'Despesa de {expense.owner_expenses} aprovada com sucesso')
    return redirect ('expense:index')

@login_required(login_url='expense:login')
def recused(request, expense_id):
    expense = get_object_or_404(Expenses, pk=expense_id)

    # Validation 1: Can not recuse own expenses
    if expense.owner_expenses == request.user:
        messages.error(request, 'Você não pode recusar as próprias despesas')
        return redirect('expense:expense', expense_id=expense_id)
    
    # Validation 2: Is need be of same team
    if not PermissionMixin.can_approve_expense(request.user, expense):
        messages.error(request, "Você não pode aprovar despesas de outra equipe")
        return redirect("expenses:index")
    
    # Validation 3: The expense status must be pending
    if expense.status_id != 4:
        messages.error(request, 'Só é possível recusar despesas pendentes')
        return redirect("expense:expense", expense_id=expense_id)
    
    form_action = reverse('expense:recused', kwargs={'expense_id': expense_id})

    if request.method == 'POST':
        
        form = AlertRecusedForm(request.POST)
        
        context = dict(
            form=form,
            form_action=form_action,
        )

        print(context)

        if form.is_valid():        
            message = form.save(commit=False) # Grarante que eu não salve na base de dados ainda
            message.expense = expense # Informo para expense.owner que esse contato pertence a esse usuário
            message.save()

            expense.status = 6 #type: ignore
            expense.save(update_fields=['status_id'])

            return redirect('expense:index')

        return render(
        request,
        'expenses/pages/alert_form.html',
        context,
        )

    context = dict(
        form=AlertRecusedForm(),
        form_action=form_action
    )

    return render(
        request,
        'expenses/pages/alert_form.html',
        context, 
        )