from django.shortcuts import render, redirect, get_object_or_404
from expenses.form import ExpenseForm, AlertRecusedForm
from expenses.models import Expenses, Status, ExpenseAudit
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from utils.conditions import Conditions #type: ignore
from django.http import HttpResponseForbidden
from utils.mixin import PermissionMixin
from utils.audit import Auditing

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
            expense.enterprise = request.user.profile.enterprise
            condition = Conditions(expense)
            cycle_id = condition.verify()

            if cycle_id is not None:
                expense.cycle_id = cycle_id
                
            expense.save()

            Auditing(expense, request, "CREATED")
            messages.success(request, "DESPESA LANÇADA COM SUCESSO", extra_tags='fa-circle-check')
            return redirect('expense:create')
        
        return render(
        request,
        'expenses/pages/create_expense.html',
        context,
        )

    context = dict(
        form=ExpenseForm(),
        title_page="CRIAR DESPESA",
        is_expense_form=True,
    )

    return render(
        request,
        'expenses/pages/create_expense.html',
        context, 
        )

@login_required(login_url='expense:login')
def expense_update(request, expense_id):
    status_pendding = get_object_or_404(Status, name='PENDENTE')
    expense = Expenses.objects.filter(pk=expense_id, owner_expenses=request.user, status__name__in=['PENDENTE', 'RECUSADO']).first()

    if not expense:
        return HttpResponseForbidden('Not Permission')

    if request.method == "POST":
        form = ExpenseForm(request.POST, request.FILES, instance=expense)
        if form.is_valid():
            updated_expense = form.save(commit=False)
            updated_expense.owner_expenses = request.user

            condition = Conditions(expense)
            cycle_id = condition.verify()
            if cycle_id is not None:
                updated_expense.cycle_id = cycle_id

            expense.status = status_pendding

            updated_expense.save()
            Auditing(expense, request, "UPDATED")

            messages.success(request, "Despesa atualizada")
            return redirect('expense:index')
        
    else:
        form = ExpenseForm(instance=expense)
    
    context = {
        'form': form,
        'expense':expense,
        'title_page':"ATUALIZAR DESPESA",
        'is_expense_form': True,
    }

    return render(
        request,
        'expenses/pages/create_expense.html',
        context,      
    )

@login_required(login_url='expense:login')
def expense_delete(request, expense_id):

    expense = get_object_or_404(
                Expenses,
                pk=expense_id,
                owner_expenses=request.user,
                )
    
    last_audit = (
        ExpenseAudit.objects
        .filter(expense=expense)
        .order_by('-created_at')
        .first()
    )
    print(last_audit)
    if last_audit and last_audit.is_checked:
        return HttpResponseForbidden('Not authorization')
    
    confirmation = request.POST.get('confirmation', 'no')
    print('confirmation', confirmation)


    if confirmation == 'yes':
        Auditing(expense, request, "DELETED")
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
    status_approved = get_object_or_404(Status, name='APROVADO')


    if PermissionMixin.is_operator(request.user):
        # Validation 1: Can not approve own expenses
        if expense.owner_expenses == request.user:
            messages.error(request, 'Você não pode aprovar as próprias despesas')
            return redirect('expense:expense', expense_id=expense_id)
        
    if PermissionMixin.is_manager(request.user):
        # Validation 2: Is need be of same team
        if not PermissionMixin.can_approve_expense(request.user, expense):
            messages.error(request, "Você não pode aprovar despesas de outra equipe")
            return redirect("expense:index")


    # Approve
    expense.status = status_approved
    expense.save()
    Auditing(expense, request, "APPROVED")

    messages.success(request, f'Despesa de {expense.owner_expenses} aprovada com sucesso')
    return redirect ('expense:index')

@login_required(login_url='expense:login')
def recused(request, expense_id):
    expense = get_object_or_404(Expenses, pk=expense_id)
    status_recused = get_object_or_404(Status, name='RECUSADO')
    status_pendding = get_object_or_404(Status, name='PENDENTE')

    if PermissionMixin.is_operator(request.user):
        # Validation 1: Can not recuse own expenses
        if expense.owner_expenses == request.user:
            messages.error(request, 'Você não pode recusar as próprias despesas')
            return redirect('expense:expense', expense_id=expense_id)
    
    if PermissionMixin.is_manager(request.user):
        # Validation 2: Is need be of same team
        if not PermissionMixin.can_approve_expense(request.user, expense):
            messages.error(request, "Você não pode aprovar despesas de outra equipe")
            return redirect("expenses:index")
        
    # Validation 3: The expense status must be pending
    if expense.status != status_pendding:
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

            expense.status = status_recused #type: ignore
            expense.save()
            
            Auditing(
                    expense=expense,
                    request=request,
                    action="REJECTED", 
                    note=message,
                    )

            return redirect('expense:index')

        return render(
        request,
        'expenses/pages/alert_form.html',
        context,
        )

    context = dict(
        form=AlertRecusedForm(),
        form_action=form_action,
        expense_id=expense_id,
    )

    return render(
        request,
        'expenses/pages/alert_form.html',
        context, 
        )