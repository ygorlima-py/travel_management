from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required(login_url='expense:login')
def accept_invite(request, uuid):
    
    print(uuid)

    return render(
        request,
        'expenses/pages/registes.html',
    )