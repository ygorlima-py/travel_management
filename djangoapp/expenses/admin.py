from django.contrib import admin
from expenses import models

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
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
                'date', 'amount', 'value',
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

