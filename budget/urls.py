from django.urls import path
from .views import CategoryListCreateView, BudgetListCreateView, BudgetDetailView, index
from . import views

urlpatterns = [
    path('', index, name='index'),
    path('manage/', views.manage_budgets, name='manage-budgets'),
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('budgets/', BudgetListCreateView.as_view(), name='budget-list-create'),
    path('budgets/<int:pk>/', BudgetDetailView.as_view(), name='budget-detail'),
]

