from rest_framework.views import APIView #type:ignore
from expenses.models import Expenses
from api.serializers import ExpenseCategorySerializers
from django.db.models import Sum
from rest_framework.response import Response  #type:ignore
from rest_framework.permissions import AllowAny  #type:ignore


class ExpenseListView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        queryset = Expenses.objects.values('category__name').annotate(total=Sum('value')).order_by('-total')
        serializer = ExpenseCategorySerializers(queryset, many=True)
        
        data = serializer.data

        response_data = {
            'xValues': [item['category'] for item in data],
            'yValues': [item['total'] for item in data],
            'barColors': ["red", "green", "blue", "orange", "brown"],
            'chartName': 'Custo total (R$) X Categoria',
        }

        return Response(response_data)

