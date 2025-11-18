from rest_framework.views import APIView #type:ignore
from expenses.models import Expenses, Cycle
from api.serializers import ExpenseCategorySerializers, ExpenseMonthSerializers, ExpenseCycleSerializers
from django.db.models import Sum
from rest_framework.response import Response  #type:ignore
from rest_framework.permissions import AllowAny  #type:ignore
from django.db.models.functions import TruncMonth


class ExpenseListView(APIView):
    permission_classes = [AllowAny]

    def _get_chart_by_category(self):
        queryset = (
                    Expenses.objects
                    .values('category__name')
                    .annotate(total=Sum('value'))
                    .order_by('-total')
                    )
        
        serializer = ExpenseCategorySerializers(queryset, many=True)
        data = serializer.data

        response_data = dict(
            labels=[item['category'] for item in data],
            datasets= [{
                'label': 'R$',
                'data': [float(item['total']) for item in data],
                'borderWidth': 1,
                'backgroundColor': [
                    '#CB4335',
                    '#1F618D',
                    '#F1C40F',
                    '#27AE60', 
                    '#884EA0', 
                    '#D35400'
                    ],
            }]
        )

        return response_data
    
    def _get_chart_by_cicle(self):
        queryset = (
            Expenses.objects
            .filter(cycle__isnull=False)
            .values('cycle__name')
            .annotate(total=Sum('value'))
            .order_by('-total')
            )
        
        serializer = ExpenseCycleSerializers(queryset, many=True)
        data = serializer.data

        response_data = dict(
            labels=[item['cycle'] for item in data],
            datasets=[{
                'label': 'Valor total gasto x Ciclo R$',
                'data': [item['total'] for item in data],
                'backgroundColor': [
                    '#1F618D',
                ],
                'borderColor': [
                    '#1F618D',
                    ],
                'borderWidth': 1,
            }]
        )

        return response_data
    
    def _get_chart_by_date(self):
        queryset = (
            Expenses.objects
            .annotate(month=TruncMonth('date'))
            .values('month')
            .annotate(total=Sum('value'))
            .order_by('month')
            )
        
        serializer = ExpenseMonthSerializers(queryset, many=True)
        
        data = serializer.data

        response_data = dict(
            labels=[item['month'] for item in data],
            datasets=[{
                'label': 'Evolução mensal dos custos R$',
                'data': [item['total'] for item in data],
                'fill': False,
                'backgroundColor': [
                    '#1F618D',
                ],
                'borderColor': [
                    '#1F618D',
                    ],
                'tension': 0.1,
            }]
        )

        return response_data
    
    def _get_average_cost_per_day(self):
        queryset_expense = (
            Expenses.objects
            .filter(cycle__isnull=False)
            .values(
                'cycle__name',
                'cycle__initial_date',
                'cycle__end_date',
                )
            .annotate(total=Sum('value'))
            .order_by('-total')
            )
        
        result = []
        for row in queryset_expense:
            initial = row['cycle__initial_date']
            end = row['cycle__end_date']
            days = (end - initial).days or 1
            avg_per_day = row['total'] / days

            result.append({
                'cycle_name': row['cycle__name'],
                'avg_per_day': avg_per_day,
            })

        response_data = dict(
            labels=[item['cycle_name'] for item in result],
            datasets=[{
                'label': 'Valor médio diário x Ciclo R$',
                'data': [round(item['avg_per_day'], 2) for item in result],
                'backgroundColor': [
                    '#1F618D',
                ],
                'borderColor': [
                    '#1F618D',
                    ],
                'borderWidth': 1,
            }]
        )


        return response_data
    
    def _get_average_fuel(self):
        queryset_expense = (
            Expenses.objects
            .filter(cycle__isnull=False)
            .filter(category__name='COMBUSTÍVEL')
            .values(
                'cycle__name',
                'cycle__initial_km',
                'cycle__end_km',
                )
            .annotate(total=Sum('amount'))
            .order_by('-total')
            )
        
        result = []
        for row in queryset_expense:
            initial = row['cycle__initial_km']
            end = row['cycle__end_km']
            distance = (end - initial)
            avg_fuel = distance / row['total']

            result.append({
                'cycle_name': row['cycle__name'],
                'avg_fuel': avg_fuel,
            })

        response_data = dict(
            labels=[item['cycle_name'] for item in result],
            datasets=[{
                'label': 'Consumo médio em km/L',
                'data': [round(item['avg_fuel'], 2) for item in result],
                'backgroundColor': [
                    '#1F618D',
                ],
                'borderColor': [
                    '#1F618D',
                    ],
                'borderWidth': 1,
            }]
        )


        return response_data
    
    def _get_average_cost_fuel(self):
        queryset_expense = (
            Expenses.objects
            .filter(cycle__isnull=False)
            .filter(category__name='COMBUSTÍVEL')
            .values('cycle__name')
            .annotate(
                total_amount=Sum('amount'),
                total_value=Sum('value')
                )
            ).order_by('cycle__id')
        
        result = []
        for row in queryset_expense:
            amount = row['total_amount']
            value = float(row['total_value'])
            avg_cost = value / amount

            result.append({
                'cycle_name': row['cycle__name'],
                'avg_cost': avg_cost,
            })

        response_data = dict(
            labels=[item['cycle_name'] for item in result],
            datasets=[{
                'label': 'Custo médio de combustível / Litro R$',
                'data': [round(item['avg_cost'], 2) for item in result],
                'backgroundColor': [
                    '#1F618D',
                ],
                'borderColor': [
                    '#1F618D',
                    ],
                'borderWidth': 1,
            }]
        )


        return response_data
    
    def _get_average_cost_km(self):
        queryset_expense = (
            Expenses.objects
            .filter(cycle__isnull=False)
            .filter(category__name='COMBUSTÍVEL')
            .values(
                'cycle__name',
                'cycle__initial_km',
                'cycle__end_km',
                )
            .annotate(total_value=Sum('value'))
            ).order_by('cycle__id')
        
        result = []
        for row in queryset_expense:
            initial = row['cycle__initial_km']
            end = row['cycle__end_km']
            distance = (end - initial)
            avg_cost = row['total_value'] / distance

            result.append({
                'cycle_name': row['cycle__name'],
                'avg_cost': avg_cost,
            })

        response_data = dict(
            labels=[item['cycle_name'] for item in result],
            datasets=[{
                'label': 'Custo médio / Km R$',
                'data': [round(item['avg_cost'], 2) for item in result],
                'backgroundColor': [
                    '#1F618D',
                ],
                'borderColor': [
                    '#1F618D',
                    ],
                'borderWidth': 1,
            }]
        )


        return response_data
    
    def get(self, request):
        
        data_json = dict(
            chart_by_category=self._get_chart_by_category(),
            chart_by_cycle=self._get_chart_by_cicle(),
            chart_by_month=self._get_chart_by_date(),
            chart_average_by_day=self._get_average_cost_per_day(),
            chart_average_fuel = self._get_average_fuel(),
            chart_average_cost_fuel=self._get_average_cost_fuel(),
            chart_average_cost_km = self._get_average_cost_km(),
        )

        return Response(data_json)

