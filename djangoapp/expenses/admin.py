from django.contrib import admin
from expenses import models

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = 'name',
    ordering = '-id',

@admin.register(models.Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = 'name',
    ordering = '-id',

@admin.register(models.State)
class StateAdmin(admin.ModelAdmin):
    list_display = 'name', 'uf_name'
    ordering = 'uf_name',

@admin.register(models.Expenses)
class ExpensesAdmin(admin.ModelAdmin):
    list_display= (
                'id', 'category','supply',
                'state_uf','city','nf', 
                'date', 'amount', 'value','status',
                )
    ordering = '-id',
    list_display_links = 'id',
    list_filter = 'category', 'owner_expenses',
    readonly_fields = 'owner_expenses',

@admin.register(models.UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display= (
                'id', 'user','phone',
                'state_uf','city','fleet_number', 
                )
    ordering = '-id',
    list_display_links = 'id',
    # readonly_fields = 'user',

@admin.register(models.AlertRecused)
class AlertRecusedAdmin(admin.ModelAdmin):
    list_display = 'id', 'message', 'created_at', 'expense',
    ordering = '-id',
    list_display_links = 'id',

@admin.register(models.Cycle)
class CycleAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'initial_date', 
        'end_date', 'initial_km', 'end_km',
        'is_open', 'save_expense_auto', 'owner',
        )
    ordering = '-id',
    list_display_links = 'id',

@admin.register(models.Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name','price','description',
        'max_users', 'max_team', 'status', 
        'created_at', 'updated_at',
    )

    ordering = '-created_at',
    list_display_links = 'name',

@admin.register(models.EnterPrise)
class EnterpriseAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'cnpj', 'owner',
        'created_at', 'updated_at', 'plan_type',
        'is_active',
    )

    ordering = '-created_at',
    list_display_links = 'name',

@admin.register(models.Role)
class RolesAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'description',
        'hierarchy', 'is_active', 'created_at',
        'updated_at',
    )

    ordering = '-created_at',
    list_display_links = 'name',

@admin.register(models.Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'enterprise', 'team_manager',
        'is_active', 'created_at', 'updated_at',
        )
    
    ordering = '-created_at',
    list_display_links = 'name',

@admin.register(models.TeamInvite)
class TeamInviteAdmin(admin.ModelAdmin):
    list_display = (
        'team', 'email', 'token',
        'invited_by', 'created_at', 'expires_at',
        'accepted'
        )
    
    ordering = '-created_at',
    list_display_links = 'team',

@admin.register(models.UserEnterpriseRole)
class UserEnterPriseAdmin(admin.ModelAdmin):
    list_display = (
        'enterprise', 'role', 'user',
    )

    list_display_links = 'enterprise',

