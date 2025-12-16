from django.urls import path
from expenses import views

app_name = 'expense'

urlpatterns = [
    # Expenses URLs
    path('', views.index, name='index' ),
    path('expense/<int:expense_id>/detail', views.expense, name='expense' ),
    path('expense/<int:expense_id>/update', views.expense_update, name='expense_update' ),#type:ignore
    path('expense/<int:expense_id>/delete', views.expense_delete, name='expense_delete' ),#type:ignore
    path('expense/<int:expense_id>/approved/', views.expense_approved, name='approved'), #type:ignore
    path('expense/<int:expense_id>/recused/', views.recused, name='recused'), #type:ignore
    path('expense/create/', views.create_expense, name='create'),
    
    # User URLs
    path('user/register/', views.register, name='register'),
    path('user/complete-profile/', views.complete_profile, name='complete_profile'),
    path('user/profile/<str:username>/', views.profile, name='profile'), #type:ignore
    path('user/update/', views.user_update, name='user_update'),
    path('user/login/', views.login_view, name='login'),
    path('user/logout/', views.logout_view, name='logout'),
    path('user/reports/', views.reports, name='reports'),
    path('user/chose/', views.chose_enterprise_or_user, name='chose'),

    # Enterprise URLs
    path('enterprise/register/', views.register_enterprise, name='register_enterprise'),
    
    # Cycles URLs
    path('ciclos/', views.cycles, name='cycles'), #type:ignore
    path('ciclo/<int:cycle_id>/detail', views.cycle, name='cycle'), #type:ignore
    path('ciclos/create/', views.create_cycle, name='create_cycle'),
    path('ciclos/<int:cycle_id>/close/', views.close_cycle, name='close_cycle'), # type:ignore
    path('ciclos/<int:cycle_id>/open/', views.open_cycle, name='open_cycle'), #type:ignore
    path('ciclos/<int:cycle_id>/update/', views.cycle_update, name='cycle_update'),
    path('ciclos/<int:cycle_id>/delete/', views.cycle_delete, name='cycle_delete'),


    path('dashbords/', views.dashbords, name='dashbords'),

    # Teams URLs
    path('equipes/', views.teams, name='teams'), #type:ignore
    path('equipe/<int:team_id>/', views.team, name='team'), #type:ignore
    path('equipes/create_team', views.create_team, name='create_team'), #type:ignore
    path('equipe/<int:team_id>/update/', views.team_update, name='team_update'),
    path('equipe/<int:team_id>/delete/', views.team_delete, name='team_delete'),
    path('equipe/<int:team_id>/invite_member/', views.invite_member, name='invite_member'),
    path('equipe/<int:team_id>/user/<int:user_id>/remove_member', views.remove_member, name='remove_member'),
    path('convite/<uuid:token>/', views.accept_invite, name='accept_invite'),
]

