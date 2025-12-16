from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from expenses.form import EnterpriseRegisterForm
from expenses.models import Role, UserEnterpriseRole, UserProfile, EnterPrise

@login_required(login_url='expense:login')
def register_enterprise(request):
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

@login_required(login_url='expense:login')
def update_enterprise(request):
    enterprise = get_object_or_404(EnterPrise, owner=request.user)

    if request.method == "POST":
        form = EnterpriseRegisterForm(request.POST, instance=enterprise)
        if form.is_valid():
            form.save()

            messages.success(request, "Empresa atualizada com sucesso")
            return redirect('expense:profile', request.user.username)
        
    else:
        form = EnterpriseRegisterForm(
            instance=enterprise,
            initial={
                'name': enterprise.name,
                'cnpj': enterprise.cnpj,
                'plan_type':enterprise.plan_type,
            }
        )

    context = dict(
        form=form,
        title_page="ATUALIZAR DADOS DA  EMPRESA",   
        is_update_enterprise=True,
    )

    return render(
        request,
        'expenses/pages/register_enterprise.html',
        context, 
    )

