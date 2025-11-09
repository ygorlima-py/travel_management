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
                'date', 'amount', 'value'
                )
    ordering = '-id',
    list_display_links = 'id', 