from django.http import Http404
from django.conf import settings
from expenses.models import Team, EnterPrise
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

@login_required(login_url='expense:login')
def teams(request):
    enterprise = EnterPrise.objects.filter(owner=request.user).first()
    teams = Team.objects.filter(enterprise=enterprise)
    
    context = {
        'teams': teams,
    }

    return render (
        request=request,
        template_name='expenses/pages/teams.html',
        context=context,
    )

