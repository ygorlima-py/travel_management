from django.urls import path
from expenses import views

app_name = 'expense'

urlpatterns = [
    path('', views.index, name='index' ),
    path('expense/<int:expense_id>/detail', views.expense, name='expense' ),
    path('expense/create/', views.create, name='create'),
    path('expense/register/', views.register, name='register'),

    path('user/profile/<str:username>', views.profile, name='profile'), #type:ignore
    path('user/update/', views.user_update, name='user_update'),
    
]