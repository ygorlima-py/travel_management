from django.urls import path
from expenses import views

app_name = 'expense'

urlpatterns = [
    path('', views.index, name='index' ),
    path('expense/<int:expense_id>/detail', views.expense, name='expense' ),
    path('expense/<int:expense_id>/update', views.expense_update, name='expense_update' ),#type:ignore
    path('expense/<int:expense_id>/delete', views.expense_delete, name='expense_delete' ),#type:ignore
    path('expense/<int:expense_id>/approved/', views.expense_approved, name='approved'), #type:ignore
    path('expense/<int:expense_id>/recused/', views.recused, name='recused'), #type:ignore
    path('expense/create/', views.create_expense, name='create'),
    path('expense/categories/', views.categories, name='categories'),
    
    path('user/register/', views.register, name='register'),
    path('user/profile/<str:username>', views.profile, name='profile'), #type:ignore
    path('user/update/', views.user_update, name='user_update'),
    path('user/login/', views.login_view, name='login'),
    path('user/logout/', views.logout_view, name='logout'),

    
]