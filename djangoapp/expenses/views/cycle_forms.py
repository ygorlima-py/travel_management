from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from expenses.form import CreateCycle, Cycle

@login_required(login_url='expense:login')
def create_cycle(request):
    form_action = reverse('expense:create_cycle')

    if request.method == 'POST':
        
        form = CreateCycle(request.POST)
        
        context = dict(
            form=form,
            form_action=form_action,
        )

        if form.is_valid():        
            cycle = form.save(commit=False) # Grarante que eu não salve na base de dados ainda
            cycle.owner = request.user # Informo para expense.owner que esse contato pertence a esse usuário
            cycle.save()
            return redirect('expense:cycles')

        return render(
        request,
        'expenses/pages/create_cycle.html',
        context,
        )

    context = dict(
        form=CreateCycle(),
        title_page="CRIAR CICLO",
    )

    return render(
        request,
        'expenses/pages/create_cycle.html',
        context, 
        )

@login_required(login_url='expense:login')
def cycle_update(request, cycle_id):
    cycle = get_object_or_404(Cycle.objects.for_user(request.user).filter(pk=cycle_id))
    
    if request.method == "POST":
        form = CreateCycle(request.POST, instance=cycle)
        if form.is_valid():
            update_cycle = form.save(commit=False)
            update_cycle.owner_id = request.user.id
            update_cycle.save()

            messages.success(request, "Ciclo atualizado")
            return redirect('expense:cycle_update', cycle_id=cycle.pk)
        
    else:
        form = CreateCycle(
            instance=cycle,
            initial={
                'name': cycle.name,
                'initial_date': cycle.initial_date.strftime('%Y-%m-%d'),
                'end_date': cycle.end_date.strftime('%Y-%m-%d'),
                'initial_km': cycle.initial_km,
                'end_km': cycle.end_km,
                'save_expense_auto': cycle.save_expense_auto,
            })
    
    context = {
        'form': form,
        'cycle':cycle,
        'title_page': "ATUALIZAR CICLO",
    }

    return render(
        request,
        'expenses/pages/create_cycle.html',
        context,      
    )

@login_required(login_url='expense:login')
def cycle_delete(request, cycle_id):
    # 1) Busca o contato pelo id; se não existir (ou show=False), retorna 404
    cycle = get_object_or_404(Cycle.objects.for_user(request.user).filter(pk=cycle_id))
    
    
    confirmation = request.POST.get('confirmation', 'no')

    if confirmation == 'yes':
        cycle.delete()
        return redirect('expense:cycles')

    return render(
        request,
        'expenses/pages/cycle.html',
        {
            'cycle': cycle,
            'confirmation': confirmation,
            'user': cycle.owner,
        }
    )