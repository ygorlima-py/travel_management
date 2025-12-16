from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from utils.mixin import PermissionMixin
from django.contrib import messages
from expenses.form import CreateTeam, TeamInviteForm # type:ignore
from expenses.models import UserEnterpriseRole, Team, UserProfile, Expenses
from django.core.paginator import Paginator

@login_required(login_url='expense:login')
def create_team(request):
    
    user_enterprises = UserEnterpriseRole.objects.filter(
        user=request.user,
        role__name='COMPANY_ADMIN'
    ).select_related('enterprise')

    if not user_enterprises.exists():
        messages.error(request, 'É necessário criar uma empresa para ter uma equipe' )
        return redirect('expense:register_enterprise')
    
    if request.method == 'POST':    
        form = CreateTeam(request.POST, user=request.user)
        
        if form.is_valid():        
            team = form.save(commit=False) # Grarante que eu não salve na base de dados ainda
            team.team_manager = request.user # Informo para team_manager que esse time pertence a esse usuário
            team.save()

            profile, created = UserProfile.objects.get_or_create(user=request.user)
            profile.team = team
            profile.save()    
            
            messages.success(request, 'Equipe criada com sucesso')
            return redirect('expense:teams')
        
        context = dict(
            form=form,
            form_action=reverse('expense:create_team'),
            title_page="CRIAR EQUIPE",
        )

        return render(
        request,
        'expenses/pages/create_team.html',
        context,
        )

    context={
        'form': CreateTeam(user=request.user),
        'form_action': reverse('expense:create_team'),
        'title_page':"CRIAR EQUIPE",
    }

    return render(
        request,
        'expenses/pages/create_team.html',
        context, 
        )

@login_required(login_url='expense:login')
def team_update(request, team_id):
    team = get_object_or_404(Team, pk=team_id, enterprise=request.user.profile.enterprise)
    
    if request.method == "POST":
        form = CreateTeam(request.POST, instance=team)
        if form.is_valid():
            update_team = form.save(commit=False)
            update_team.team_manager = request.user.id
            update_team.save()

            messages.success(request, "Equipe atualizada")
            return redirect('expense:team', team_id=team.pk)
        
    else:
        form = CreateTeam(
            instance=team,
            initial={
                'name': team.name,
                'cost_center': team.cost_center,
                'enterprise': team.enterprise,
            })
    
    context = {
        'form': form,
        'team':team,
        'title_page': 'ATUALIZAR EQUIPE',
    }

    return render(
        request,
        'expenses/pages/create_cycle.html',
        context,      
    )

@login_required(login_url='expense:login')
def team_delete(request, team_id):
    user = request.user
    team = get_object_or_404(Team, pk=team_id)


    if not PermissionMixin.can_exclude_team(user, team):
        messages.error(request, 'Você não pode excluir essa equipe')
        return redirect('expense:teams')
    
    members = UserProfile.objects.filter(team=team)
    expenses = Expenses.objects.filter(owner_expenses__profile__team=team)
    page_number = request.GET.get("page")
    paginator = Paginator(expenses, 25)  # Show 25 contacts per page.
    page_obj = paginator.get_page(page_number)
    role = PermissionMixin.get_user_role(request.user)
        

    # GET: Exibe página de confirmação
    if request.method == 'POST':
    
        confirmation = request.POST.get('confirmation', 'no')

        if confirmation == 'yes':   
            team.delete()
            messages.success(request, 'Equipe excluida com sucesso')
            return redirect('expense:teams')

    return render(
        request,
        'expenses/pages/team.html',
        {
            'team': team,
            'confirmation': confirmation,
            'user': user,
            'members': members,
            'page_obj': page_obj,
            'role': role,
        }
    )

