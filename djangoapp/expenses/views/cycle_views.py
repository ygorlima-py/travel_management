from django.http import Http404
from django.contrib.auth.models import User
from expenses.models import Cycle
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

@login_required(login_url='expense:login')
def cycles(request, username):
    user = get_object_or_404(User, username=username)
    cycles = Cycle.objects.filter(owner=user)
        
    context = {
        'cycles': cycles,
    }

    return render (
        request=request,
        template_name='expenses/pages/cycles.html',
        context=context,
    )