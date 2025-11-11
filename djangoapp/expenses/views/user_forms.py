from django.shortcuts import render, redirect
from django.contrib import messages, auth
from expenses.form import RegisterForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

''' Route for the user to register on the platform '''
def register(request):
    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Usuário Cadastrado com sucesso')
            return redirect('contact:login')



    return render(
        request,
        'expenses/pages/register.html',
        {
            'form':form,
        }
    )
