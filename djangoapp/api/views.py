from rest_framework.views import APIView #type:ignore
from expenses.models import Expenses
from api.serializers import ExpenseCategorySerializers, ExpenseMonthSerializers
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

        response_data = {
            'xValues': [item['category'] for item in data],
            'yValues': [item['total'] for item in data],
            'barColors': ["red", "green", "blue", "orange", "brown"],
            'chartName': 'Custo total (R$) X Categoria',
        }

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

        response_data = {
            'xValues': [item['month'] for item in data],
            'yValues': [item['total'] for item in data],
            'chartName': 'Custo total (R$) X Mês',
        }

        return response_data

    def get(self, request):
        
        data_json = dict(
            chart_by_category=self._get_chart_by_category(),
            chart_by_month=self._get_chart_by_date(),
        )

        return Response(data_json)

