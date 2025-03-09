from django.contrib import admin
from .models import Budget, Category, BudgetAllocation, Gifts, Usage

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'amount', 'start_date', 'end_date', 'created_at']
    list_filter = ['name', 'amount', 'end_date']
    search_fields = ['name', 'amount']
    raw_id_fields = ['user']
    date_hierarchy = 'created_at'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'created_at']
    list_filter = ['name']
    search_fields = ['name']
    raw_id_fields = ['user']
    date_hierachy = 'created_at'

@admin.register(BudgetAllocation)
class BudgetAllocationAdmin(admin.ModelAdmin):
    list_display = ['category', 'allocated_amount']
    list_filter = ['category', 'allocated_amount']
    search_fields = ['category', 'allocated_amount']

admin.site.register(Gifts)
admin.site.register(Usage)
