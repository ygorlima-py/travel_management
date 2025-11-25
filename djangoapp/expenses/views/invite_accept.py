from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from expenses.models import TeamInvite
from django.contrib import messages

@login_required(login_url='expense:login')
def accept_invite(request, token):
    invite = get_object_or_404(TeamInvite, token=token)

    if invite.is_valid():
        messages.success(request,'Convite Válido')
        print(invite.email)
        print(invite.token)
        print(invite.created_at)
    else:
        messages.error(request,'Convite Inválido')

    return render(
        request,
        'expenses/pages/register.html',
    )