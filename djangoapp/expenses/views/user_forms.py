from django.shortcuts import render, redirect
from django.contrib import messages, auth
from expenses.form import RegisterForm, UpdateFormUser, UserProfileForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.contrib.auth.models import User
from expenses.models import UserProfile, UserEnterpriseRole, Role

''' Route for the user to register on the platform '''
def register(request): 
    invite_email = request.session.get('invite_email')
    
    form = RegisterForm()

    if invite_email:
        form.initial['email'] = invite_email
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        invite_token = request.session.get('invite_token')

        if form.is_valid():
            user = form.save()
            
            UserProfile.objects.get_or_create(user=user)

            auth.login(request, user)
            messages.success(request, 'Usuário Cadastrado com sucesso')
            
            if invite_token:
                del request.session['invite_token']
                del request.session['invite_email']               
                return redirect('expense:accept_invite', token=invite_token)           
            
            return redirect('expense:chose')

    return render(
        request,
        'expenses/pages/register.html',
        {
            'form':form,
            'is_register': True,
            'title_page': 'CADASTRAR'
        }
    )

@login_required(login_url='expense:login')
def complete_profile(request):
    
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)

        if form.is_valid():
            form.save()
            operator_role = Role.objects.filter(hierarchy=40).first()
            UserEnterpriseRole.objects.get_or_create(
                user=request.user,
                role=operator_role,
                enterprise=None,
            )

            messages.success(request, 'Perfil de usuario preechido com sucesso')
            return redirect('expense:index')
        
    else:
        form = UserProfileForm(instance=profile)
    
    context = dict(
        form=form,
        is_profile_complete=True,
        title_page="COMPLETAR PERFIL"
    )

    return render(
        request,
        'expenses/pages/complete_profile.html',
        context=context,
    )

@login_required(login_url='expense:login')
def user_update(request):
    form = UpdateFormUser(instance=request.user)

    if request.method == 'POST':
        form = UpdateFormUser(
            data=request.POST,
            instance=request.user,
        )

        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado com sucesso')
            return redirect('expense:profile', username=request.user.username)

    return render(
        request,
        'expenses/pages/update_user.html',
        {
            'form':form,
            'is_user_update': True,
            'title_page': 'ATUALIZAR DADOS DO USUÁRIO'
        }
    )

""" Rota para o usuário logar """
def login_view(request):
    form = AuthenticationForm(request)

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        invite_token = request.session.get('invite_token')

        if form.is_valid(): # Return bool verifying if data digited is valid
            user = form.get_user() # Select user form
            auth.login(request, user) # Authentication logging in as user
            messages.success(request,'Você está logado') # Message success to user log
            
            # If user have a team invite
            if invite_token:
                del request.session['invite_token'] # delete token of session
                return redirect('expense:accept_invite', token=invite_token) # Redirect to view with invite token
            
            return redirect('expense:index') # Redirect to page home
        
        else:
            messages.error(request, 'Login Invalido')




    return render(
        request,
        'expenses/pages/login.html',
        {
            'form':form,
            'is_login': True,
        }
    )

@login_required(login_url='expense:login')
def logout_view(request):
    auth.logout(request)
    return redirect('expense:login')
