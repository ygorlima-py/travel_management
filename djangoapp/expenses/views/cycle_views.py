from django.http import Http404
from django.contrib.auth.models import User
from expenses.models import Cycle, Expenses
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from utils.calculation import Calculation 
from utils.mixin import PermissionMixin

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

    # Source - https://stackoverflow.com/a
    # Posted by Platinum Azure, modified by community. See post 'Timeline' for change history
    # Retrieved 2025-11-13, License - CC BY-SA 4.0
    obj, created = Cycle.objects.update_or_create(
        pk=cycle_id,
        defaults={'is_open': False},
    )

    if obj is None:
        raise Http404()
    
    if created == False:
        return redirect("expense:cycles")
    
    
def open_cycle(request, cycle_id):

    # Source - https://stackoverflow.com/a
    # Posted by Platinum Azure, modified by community. See post 'Timeline' for change history
    # Retrieved 2025-11-13, License - CC BY-SA 4.0
    obj, created = Cycle.objects.update_or_create(
        pk=cycle_id,
        defaults={'is_open': True},
    )

    if obj is None:
        raise Http404()
    
    if created == False:
        return redirect("expense:cycles")
    
    