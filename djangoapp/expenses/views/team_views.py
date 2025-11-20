from django.http import Http404
from django.conf import settings
from expenses.models import Team, EnterPrise, Expenses
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

@login_required(login_url='expense:login')
def team(request, team_id):
    team = get_object_or_404(Team, pk=team_id)   
    expenses = Expenses.objects.filter(
        owner_expenses=request.user,
        )
    
    # calculation = Calculation(team, expenses).all()

    context = {
        'team': team,
        'expenses': expenses,
        # 'calculation': calculation,
    }

    return render (
        request=request,
        template_name='expenses/pages/team.html',
        context=context,
    )

