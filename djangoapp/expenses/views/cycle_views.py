from django.http import Http404
from django.contrib.auth.models import User
from expenses.models import Cycle, Expenses
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from utils.calculation import Calculation 

@login_required(login_url='expense:login')
def cycles(request):
    cycles = Cycle.objects.filter(owner=request.user)
        
    context = {
        'cycles': cycles,
    }

    return render (
        request=request,
        template_name='expenses/pages/cycles.html',
        context=context,
    )

@login_required(login_url='expense:login')
def cycle(request, cycle_id):
    cycle = get_object_or_404(Cycle, id=cycle_id)   
    expenses = Expenses.objects.filter(
        owner_expenses=request.user,
        cycle=cycle
        )
    
    calculation = Calculation(cycle, expenses).all()

    context = {
        'cycle': cycle,
        'expenses': expenses,
        'calculation': calculation,
    }

    return render (
        request=request,
        template_name='expenses/pages/cycle.html',
        context=context,
    )