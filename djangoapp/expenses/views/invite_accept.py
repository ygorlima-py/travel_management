from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from expenses.models import TeamInvite, UserEnterpriseRole, Role, UserProfile
from django.contrib import messages

User = get_user_model()


def accept_invite(request, token):
    invite = get_object_or_404(TeamInvite, token=token)
    
    # Check if invite is valid 
    if not invite.is_valid():
        messages.error(request,'Convite Inválido')
        return redirect('expense:login')
    
    # Check if user is authenticated
    if request.user.is_authenticated:
        
        # Check if email address user is the same as the email invite
        if request.user.email != invite.email: 
            messages.error(request,'Usuário divergente do email de convite')
            return redirect('expense:login')

        # Add member and create profile
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        profile.team = invite.team
        profile.save()

        # Add Enterprise and Role in the User
        role = invite.role
        UserEnterpriseRole.objects.get_or_create(
            enterprise=invite.team.enterprise,
            role=role,
            user=request.user
        )

        # Mark true to accept invite
        invite.accepted = True
        invite.save(update_fields=['accepted'])

        messages.success(request, f'Você entrou na equipe {invite.team.name}')
        return redirect('expense:index')

    # If user is not logged in but have account
    if User.objects.filter(email=invite.email).exists():
        request.session['invite_token'] = str(token)
        messages.info(request, 'Faça o loggin com sua conta e clique novamente no link')
        return redirect('expense:login')
    
    # If user dont have account
    else:
        request.session['invite_token'] = str(token)
        request.session['invite_email'] = invite.email
        messages.info(request, 'Crie uma conta com esse mesmo email e clique aqui novamente')
        return redirect('expense:register')