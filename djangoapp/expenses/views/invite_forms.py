from django.contrib.auth.decorators import login_required
from django.urls import reverse
from expenses.models import Team
from expenses.form import TeamInviteForm
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from utils.send_invite import SendInvite
from utils.mixin import PermissionMixin

@login_required(login_url='expense:login')
def invite_member(request, team_id):
    team = get_object_or_404(Team, pk=team_id)

    if PermissionMixin.can_invite_or_remove_member(request.user, team):

        if request.method == 'POST':
            form = TeamInviteForm(request.POST, team=team)

            if form.is_valid():
                invite = form.save(commit=False)
                invite.team = team
                invite.invited_by = request.user
                invite.save()

                send_invite = SendInvite(invite.email, team_id) # Create url in utils

                if send_invite.send_invite():
                    messages.success(request, f'Convite enviado para {invite.email} com sucesso')
                    return redirect('expense:team', team_id=team.pk)
                
            context = dict(
                form=form,
                team=team,
                form_action=reverse('expense:invite_member', args=[team_id])
            )
            return render(
                request,
                'expenses/pages/invite_member.html',
                context,     
                )

        context = dict(
            form=TeamInviteForm(team=team_id),
            team=team,
            form_action=reverse('expense:invite_member', args=[team_id]),
            title_page='CONVIDAR MEMBRO',
        )
    
    else:
        messages.error(request, 'Você não pode adicionar membros nesta equipe')
        return redirect('expense:index')
    
    
    return render(
        request,
        'expenses/pages/invite_member.html',
        context,      
    )