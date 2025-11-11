from django.http import Http404
from django.contrib.auth.models import User
from django.shortcuts import render

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