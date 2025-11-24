from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from expenses.form import CreateTeam, TeamInviteForm # type:ignore
from expenses.models import UserEnterpriseRole, Team

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

            messages.success(request, 'Equipe criada com sucesso')
            return redirect('expense:teams')
        
        context = dict(
            form=form,
            form_action=reverse('expense:create_team'),
        )

        return render(
        request,
        'expenses/pages/create_team.html',
        context,
        )

    context = dict(
        form=CreateTeam(user=request.user),
        form_action=reverse('expense:create_team')
    )

    return render(
        request,
        'expenses/pages/create_team.html',
        context, 
        )

@login_required(login_url='expense:login')
def team_update(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    
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
        'is_form_update': True,
    }

    return render(
        request,
        'expenses/pages/create_cycle.html',
        context,      
    )

# @login_required(login_url='expense:login')
# def team_delete(request, cycle_id):
#     # 1) Busca o contato pelo id; se não existir (ou show=False), retorna 404
#     cycle = get_object_or_404(Cycle, pk=cycle_id, owner_id=request.user)
    
#     confirmation = request.POST.get('confirmation', 'no')

#     if confirmation == 'yes':
#         cycle.delete()
#         return redirect('expense:cycles')

#     return render(
#         request,
#         'expenses/pages/cycle.html',
#         {
#             'cycle': cycle,
#             'confirmation': confirmation,
#             'user': cycle.owner,
#         }
#     )