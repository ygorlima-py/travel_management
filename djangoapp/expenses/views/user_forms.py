from django.shortcuts import render, redirect
from django.contrib import messages, auth
from expenses.form import RegisterForm, RegisterUpdateForm
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
            form.save()
            messages.success(request, 'Usuário Cadastrado com sucesso')
            return redirect('expense:profile', username=request.user.username)

    return render(
        request,
        'expenses/pages/register.html',
        {
            'form':form,
        }
    )

def user_update(request):
    form = RegisterUpdateForm(instance=request.user)

    if request.method == 'POST':
        form = RegisterUpdateForm(
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
        }
    )