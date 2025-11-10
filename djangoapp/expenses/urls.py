from django.urls import path
from expenses import views

app_name = 'expense'

urlpatterns = [
    path('', views.index, name='index' ),
    path('expense/<int:expense_id>/detail', views.expense, name='expense' ),
    path('expense/create/', views.create, name='create'),
]