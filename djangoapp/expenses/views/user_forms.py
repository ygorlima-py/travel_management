from django.shortcuts import render, redirect
from django.contrib import messages, auth
from expenses.form import RegisterForm, UpdateFormUser
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.contrib.auth.models import User


''' Route for the user to register on the platform '''
def register(request):
    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            auth.login(request, user)
            messages.success(request, 'Usuário Cadastrado com sucesso')
            return redirect('expense:chose')

    return render(
        request,
        'expenses/pages/register.html',
        {
            'form':form,
            'is_register': True,
        }
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
        }
    )

""" Rota para o usuário logar """
def login_view(request):
    form = AuthenticationForm(request)

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid(): # Retorna booleano verificando se os dados digitados são validos
            user = form.get_user() # Seleciona no banco o usuário 
            auth.login(request, user) # Faz a autentificação logando o usuário
            messages.success(request,'Você está logado') # Menssagem de sucesso do usuário logado
            return redirect('expense:index') # Redireciona para a pgina index home
        
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
