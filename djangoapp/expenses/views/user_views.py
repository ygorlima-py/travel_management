from django.http import Http404
from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='expense:login')
def profile(request, username):
    user = User.objects.filter(username=username).first() 
    
    if user is None:
        raise Http404("Perfil não encontrado")
    
    context = {
        'user': user,
    }

    return render (
        request=request,
        template_name='expenses/pages/profile.html',
        context=context,
    )


@login_required(login_url='expense:login')
def reports(request):
    if request.method == 'POST':
        initial_date = request.POST.get('initial_date')
        end_date = request.POST.get('end_date')

        print(initial_date, end_date)

    context = {
        'help_text_initial': 'Selecione a data inicial do periodo que deseja extrair o relatório',
        'help_text_end': 'Selecione a data final do periodo que deseja extrair o relatório'
    }
    return render (
        request=request,
        template_name='expenses/pages/reports.html',
        context=context
    )
