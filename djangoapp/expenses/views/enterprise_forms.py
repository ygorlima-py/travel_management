from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from expenses.form import EnterpriseRegisterForm
from expenses.models import Role, UserEnterpriseRole, UserProfile

@login_required(login_url='expense:login')
def register_enterprise(request):
    # form_action = reverse('expense:create_cycle')

    if request.method == 'POST':
        
        form = EnterpriseRegisterForm(request.POST)
        
        context = dict(
            form=form,
            # form_action=form_action,         
        )

        if form.is_valid():        
            enterprise = form.save(commit=False)
            enterprise.owner = request.user # fill in the enterprise.owner field with the owner.
            enterprise.save()

            profile = UserProfile.objects.get(user=request.user)
            profile.enterprise = enterprise # fill in the company field with the company created by the user..
            profile.save()

            owner_role = Role.objects.get(name='COMPANY_ADMIN')

            UserEnterpriseRole.objects.create(
                user=request.user,
                enterprise=enterprise,
                role=owner_role,
            )
            
            messages.success(request, "Empresa cadastrada com sucesso")
            return redirect('expense:index')

        return render(
        request,
        'expenses/pages/register_enterprise.html',
        context,
        )

    context = dict(
        form=EnterpriseRegisterForm(),
        title_page="CADASTRAR EMPRESA",   
        is_register_enterprise=True,
    )

    return render(
        request,
        'expenses/pages/register_enterprise.html',
        context, 
        )