from rest_framework.views import APIView #type:ignore
from expenses.models import Expenses, Cycle
from api.serializers import ExpenseCategorySerializers, ExpenseMonthSerializers, ExpenseCycleSerializers
from django.db.models import Sum, Avg, Count
from rest_framework.response import Response  #type:ignore
from rest_framework.permissions import IsAuthenticated
from django.db.models.functions import TruncMonth
from utils.mixin import PermissionMixin

class DashbordView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        role = PermissionMixin.get_user_role(user)

        if role == 'OPERATOR':
            data = self._get_operator_dashbord(user)
        elif role == 'MANAGER':
            data = self._get_manager_dashbord(user)
        elif role == 'COMPANY_ADMIN':
            data = self._get_company_admin_dashbord(user)
        else:
            return Response({'error': 'Sem Permissão'}, status=403) 
        
        return Response(data)
    
    """Methods to find role user and queryset data"""
    def _get_operator_dashbord(self, user):
        expenses = Expenses.objects.filter(owner_expenses=user)

        return {
            'total_pending': self._total_by_status(expenses, 'PENDENTE'),
            'total_approved_month': self._total_aproved_month(expenses, 'APROVADO'),
            'current_cicle': self._current_cicle(user),
            'chart_by_category': self._chart_category(expenses),
            'chart_by_month': self._get_chart_by_date(expenses),
            'chart_by_cicle': self._get_chart_by_cicle(expenses),
            'chart_average_by_day': self._get_average_cost_per_day(expenses),
            'chart_average_fuel': self._get_average_fuel(expenses),
            'chart_average_cost_fuel': self._get_average_cost_fuel(expenses),
            'chart_average_cost_km': self._get_average_cost_km(expenses),
        }
    
    def _get_manager_dashbord(self, user):
        # Get team 
        team = PermissionMixin.get_user_team(user)
        # Filter expenses of team
        expenses = Expenses.objects.filter(owner_expenses__profile__team=team)

        return {
            'total_pending_team': self._total_by_status(expenses, 'PENDENTE'),
            'total_approved_month': self._total_aproved_month(expenses, 'APROVADO'),
            'awaiting_approvval': self._awaiting_approval(expenses, user),
            'current_cicle_manager': self._current_cicle(user),
            'team_members': self._team_members(team),
            'ranking_cost': self.ranking_cost(team),
            'chart_by_category': self._chart_category(expenses),
            'chart_by_month': self._get_chart_by_date(expenses),
            'chart_by_cicle': self._get_chart_by_cicle(expenses),
            'chart_average_by_day': self._get_average_cost_per_day(expenses),
            'chart_average_fuel': self._get_average_fuel(expenses),
            'chart_average_cost_km': self._get_average_cost_km(expenses),
            'chart_per_member': self.chart_per_member(expenses),
        }
    
    def _get_company_admin_dashbord(self, user):
        enterprise = PermissionMixin.get_user_enterprise(user)
        expenses = Expenses.objects.filter(owner_expenses__profile__team__enterprise=enterprise)

        return {
            'total_enterprise': expenses.aggregate(Sum('value'))['value__sum'] or 0,
            'total_per_team': self._total_per_team(enterprise),
            'total_per_month': self._total_per_month(expenses),
            'team_registers': self._teams_registers(enterprise),
            'projection_month': self._projection_end_month(expenses),
            'chart_by_category': self._chart_category(expenses),
            'chart_by_month': self._get_chart_by_date(expenses),
            'chart_by_cicle': self._get_chart_by_cicle(expenses),
            'chart_average_by_day': self._get_average_cost_per_day(expenses),
            'chart_average_fuel': self._get_average_fuel(expenses),
            'chart_average_cost_km': self._get_average_cost_km(expenses),
            'chart_per_tem': self._chart_per_team(enterprise),
        }

    """Shared auxiliary methods"""
    def _get_status_id(self, status_name):
        from expenses.models import Status
        status = Status.objects.filter(name=status_name).first()
        return status.id 

    def _total_by_status(self, queryset, status_name):
        status_id = self._get_status_id(status_name)
        return queryset.filter(status_id=status_id).aggregate(Sum('value'))['value__sum'] or 0
    
    def _total_aproved_month(self, queryset, status_name):
        from datetime import datetime
        current_month = datetime.now().month
        status_id = self._get_status_id(status_name)

        return queryset.filter(status_id=status_id, date__month=current_month).aggregate(Sum('value'))['value__sum'] or 0

    def _current_cicle(self, user):
        cicle = Cycle.objects.filter(owner=user, is_open=True).first()
        return {'name': cicle.name if cicle else None}
    
    def _chart_category(self, queryset):
        data = queryset.values('category__name').annotate(total=Sum('value'))
        return {
            'labels': [item['category__name'] for item in data],
            'datasets': [{
                'data': [float(item['total']) for item in data],
                'backgroundColor': [
                    '#CB4335',
                    '#1F618D',
                    '#F1C40F',
                    '#27AE60',
                    '#884EA0', 
                    '#D35400',
                    ],
            }]
        }
    
    def _get_chart_by_date(self, queryset):
        data = (
            queryset
            .annotate(month=TruncMonth('date'))
            .values('month')
            .annotate(total=Sum('value'))
            .order_by('month')
        )
        
        serializer = ExpenseMonthSerializers(data, many=True)
        serialized_data = serializer.data

        return {
            'labels': [item['month'] for item in serialized_data],
            'datasets': [{
                'label': 'Evolução mensal dos custos R$',
                'data': [item['total'] for item in serialized_data],
                'fill': False,
                'backgroundColor': ['#1F618D'],
                'borderColor': ['#1F618D'],
                'tension': 0.1,
            }]
        }
    
    def _get_chart_by_cicle(self, queryset):
        data = (
            queryset
            .filter(cycle__isnull=False)
            .values('cycle__name')
            .annotate(total=Sum('value'))
            .order_by('-total')
        )
        
        serializer = ExpenseCycleSerializers(data, many=True)
        serialized_data = serializer.data

        return {
            'labels': [item['cycle'] for item in serialized_data],
            'datasets': [{
                'label': 'Valor total gasto x Ciclo R$',
                'data': [item['total'] for item in serialized_data],
                'backgroundColor': ['#1F618D'],
                'borderColor': ['#1F618D'],
                'borderWidth': 1,
            }]
        }
    
    def _get_average_cost_per_day(self, queryset):
        data = (queryset
                .filter(cycle__isnull=False)
                .values('cycle__name', 'cycle__initial_date', 'cycle__end_date')
                .annotate(total=Sum('value'))
                .order_by('-total'))
        
        result = []
        for row in data:
            initial = row['cycle__initial_date']
            end = row['cycle__end_date']
            days = (end - initial).days or 1
            avg_per_day = row['total'] / days
            result.append({'cycle_name': row['cycle__name'], 'avg_per_day': avg_per_day})

        return {
            'labels': [item['cycle_name'] for item in result],
            'datasets': [{
                'label': 'Valor médio diário x Ciclo R$',
                'data': [round(item['avg_per_day'], 2) for item in result],
                'backgroundColor': ['#1F618D'],
                'borderColor': ['#1F618D'],
                'borderWidth': 1,
            }]
        }
    
    def _get_average_fuel(self, queryset):
        data = (queryset
                .filter(cycle__isnull=False, category__name='COMBUSTÍVEL')
                .values('cycle__name', 'cycle__initial_km', 'cycle__end_km')
                .annotate(total=Sum('amount'))
                .order_by('-total'))
        
        result = []
        for row in data:
            distance = (row['cycle__end_km'] - row['cycle__initial_km'])
            avg_fuel = distance / row['total'] if row['total'] else 0
            result.append({'cycle_name': row['cycle__name'], 'avg_fuel': avg_fuel})

        return {
            'labels': [item['cycle_name'] for item in result],
            'datasets': [{
                'label': 'Consumo médio em km/L',
                'data': [round(item['avg_fuel'], 2) for item in result],
                'backgroundColor': ['#1F618D'],
                'borderColor': ['#1F618D'],
                'borderWidth': 1,
            }]
        }
    
    def _get_average_cost_fuel(self, queryset):
        data = (queryset
                .filter(cycle__isnull=False, category__name='COMBUSTÍVEL')
                .values('cycle__name')
                .annotate(total_amount=Sum('amount'), total_value=Sum('value'))
                .order_by('cycle__id'))
        
        result = []
        for row in data:
            avg_cost = float(row['total_value']) / row['total_amount'] if row['total_amount'] else 0
            result.append({'cycle_name': row['cycle__name'], 'avg_cost': avg_cost})

        return {
            'labels': [item['cycle_name'] for item in result],
            'datasets': [{
                'label': 'Custo médio de combustível / Litro R$',
                'data': [round(item['avg_cost'], 2) for item in result],
                'backgroundColor': ['#1F618D'],
                'borderColor': ['#1F618D'],
                'borderWidth': 1,
            }]
        }
    
    def _get_average_cost_km(self, queryset):
        data = (queryset
                .filter(cycle__isnull=False, category__name='COMBUSTÍVEL')
                .values('cycle__name', 'cycle__initial_km', 'cycle__end_km')
                .annotate(total_value=Sum('value'))
                .order_by('cycle__id'))
        
        result = []
        for row in data:
            distance = (row['cycle__end_km'] - row['cycle__initial_km'])
            avg_cost = row['total_value'] / distance if distance else 0
            result.append({'cycle_name': row['cycle__name'], 'avg_cost': avg_cost})

        return {
            'labels': [item['cycle_name'] for item in result],
            'datasets': [{
                'label': 'Custo médio / Km R$',
                'data': [round(item['avg_cost'], 2) for item in result],
                'backgroundColor': ['#1F618D'],
                'borderColor': ['#1F618D'],
                'borderWidth': 1,
            }]
        }

    """Specific methods of the manager"""
    def _awaiting_approval(self, queryset, user):
        status_id = self._get_status_id('APROVADO')

        return queryset.filter(status_id=status_id).exclude(owner_expenses=user).count()

    def _team_members(self, team):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        return User.objects.filter(profile__team=team).count()

    def ranking_cost(self, team):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        ranking = User.objects.filter(profile__team=team).annotate(
            total_gasto=Sum('expenses__value')
        ).order_by('-total_gasto')[:5]
        
        return [{'username': usuario.username, 'total': float(usuario.total_gasto or 0)} for usuario in ranking]

    def _chart_per_member(self, queryset):
        data = queryset.values('owner_expenses__username').annotate(total=Sum('value'))
        return {
            'labels': [item['owner_expenses__username'] for item in data],
            'datasets': [{
                'label': 'Gasto por membro R$',
                'data': [float(item['total']) for item in data],
                'backgroundColor': ['#1F618D'],
                'borderColor': ['#1F618D'],
                'borderWidth': 1,
            }]
        }

    """Specific methods of the Admin"""
    def _total_per_team(self, enterprise):
        from expenses.models import Team, UserProfile
        
        teams = Team.objects.filter(enterprise=enterprise).annotate(
            total=Sum('members__user__expenses_owner__value')
        )
        
        return [{'team': team.name, 'total': float(team.total or 0)} for team in teams]

    def _total_per_month(self, queryset):
        data = (queryset
                .annotate(month=TruncMonth('date'))
                .values('month')
                .annotate(total=Sum('value'))
                .order_by('month'))
        
        return [{'month': item['month'].strftime('%b/%y'), 'total': float(item['total'])} for item in data]

    def _teams_registers(self, enterprise):
        from expenses.models import Team
        return Team.objects.filter(enterprise=enterprise).count()

    def _chart_per_team(self, enterprise):
        from expenses.models import Team
        
        teams = Team.objects.filter(enterprise=enterprise).annotate(
            total=Sum('members__user__expenses_owner__value')
        )
        
        return {
            'labels': [team.name for team in teams],
            'datasets': [{
                'label': 'Gasto por equipe R$',
                'data': [float(team.total or 0) for team in teams],
                'backgroundColor': ['#1F618D'],
                'borderColor': ['#1F618D'],
                'borderWidth': 1,
            }]
        }

    def _projection_end_month(self, queryset):
        from datetime import datetime
        current_month = datetime.now().month
        
        total_month = queryset.filter(date__month=current_month).aggregate(Sum('value'))['value__sum'] or 0
        current_day = datetime.now().day
        days_month_qtd = 30
        
        projection = (total_month / current_day) * days_month_qtd
        return round(projection, 2)    

