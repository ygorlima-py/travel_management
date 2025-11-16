from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from expenses.form import CreateCycle

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
        form=CreateCycle()
    )

    return render(
        request,
        'expenses/pages/create_cycle.html',
        context, 
        )