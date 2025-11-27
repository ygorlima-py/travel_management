from django.http import Http404
from expenses.models import Cycle, Expenses
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from utils.calculation import Calculation 
from utils.mixin import PermissionMixin


@login_required(login_url='expense:login')
def cycles(request):
    cycles = Cycle.objects.for_user(request.user)
        
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
    
    cycle = get_object_or_404(Cycle.objects.for_user(request.user).filter(pk=cycle_id))

    if PermissionMixin.is_manager(request.user) or PermissionMixin.is_company_admin(request.user):
        expenses = Expenses.objects.filter(cycle=cycle)

    else:    
        expenses = Expenses.objects.for_user(request.user).filter(cycle=cycle)
    

    role = PermissionMixin.get_user_role(request.user)
    calculation = Calculation(cycle, expenses).all()

    context = {
        'cycle': cycle,
        'expenses': expenses,
        'calculation': calculation,
        'role': role,
    }

    return render (
        request=request,
        template_name='expenses/pages/cycle.html',
        context=context,
    )

def close_cycle(request, cycle_id):

    cicle = get_object_or_404(
        Cycle.objects.for_user(request.user).filter(pk=cycle_id),
        ) 

    if cicle.is_open:
        cicle.is_open = False
        cicle.save()

    return redirect("expense:cycles")
    
    
def open_cycle(request, cycle_id):
    cicle = get_object_or_404(
        Cycle.objects.for_user(request.user).filter(pk=cycle_id),
    ) 
    
    if not cicle.is_open:
        cicle.is_open = True
        cicle.save()

    return redirect("expense:cycles")
    
    