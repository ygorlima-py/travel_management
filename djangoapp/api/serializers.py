from rest_framework import serializers

class ExpenseCategorySerializers(serializers.Serializer):
    category = serializers.CharField(source='category__name')
    total = serializers.DecimalField(max_digits=12, decimal_places=2)

class ExpenseMonthSerializers(serializers.Serializer):
    month = serializers.DateTimeField(format='%m/%Y')
    total = serializers.DecimalField(max_digits=12, decimal_places=2)