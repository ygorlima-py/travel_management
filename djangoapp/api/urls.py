from django.urls import path
from api import views

app_name = 'api'

urlpatterns = [
    path('expenses/', views.ExpenseListView.as_view(), name='expense-list'),
]