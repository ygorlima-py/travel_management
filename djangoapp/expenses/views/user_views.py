from django.http import Http404, HttpResponse
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from expenses.models import Expenses
from utils.reports import GenerateReports
from datetime import datetime
from utils.mixin import PermissionMixin

@login_required(login_url='expense:login')
def profile(request, username):
    User = get_user_model()
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
    
    role = PermissionMixin.get_user_role(request.user)

    if request.method == 'POST':
        initial_date = request.POST.get('initial_date')
        end_date = request.POST.get('end_date')
        user = request.user

        if not initial_date or not end_date:
            return redirect('expense:reports')

        initial = datetime.strptime(initial_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        queryset = Expenses.objects.for_user(user).filter(date__date__range=(initial, end))
        excel_file = GenerateReports(queryset=queryset).generate_excel()
        response = HttpResponse(
            excel_file.getvalue(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response["Content-Disposition"] = 'attachment; filename="relatorio_despesas.xlsx"' 
    
        return response

    context = {
        'help_text_initial': 'Selecione a data inicial do periodo que deseja extrair o relatório',
        'help_text_end': 'Selecione a data final do periodo que deseja extrair o relatório',
        'role': role,
    }
    return render (
        request=request,
        template_name='expenses/pages/reports.html',
        context=context,
    )

@login_required(login_url='expense:login')
def chose_enterprise_or_user(request):
    
    return render (
        request=request,
        template_name='expenses/pages/chose_register.html',
    )
