from django.urls import path
from .views import CategoryListCreateView, BudgetListCreateView, BudgetDetailView, index, BudgetListView, BudgetCreateView, category_list, category_create
from . import views

urlpatterns = [
    path('', index, name='index'),
    path('manage/', views.manage_budgets, name='manage-budgets'),
    path('budgets/', BudgetListCreateView.as_view(), name='budget-list-create'),
    path('budgets/<int:pk>/', BudgetDetailView.as_view(), name='budget-detail'),
    path("list/", BudgetListView.as_view(), name="budget-list"),
    path("create/", BudgetCreateView.as_view(), name="budget-create"),
    path("categories/", category_list, name="category_list"),
    path("categories/<int:budget_id>/", category_list, name="category_list"),
    path("categories/add/<int:budget_id>/", category_create, name="category-create"),
    path('categories/update/<int:pk>/', views.category_update, name='category_update'),
    path('categories/delete/<int:pk>/', views.category_delete, name='category_delete'),
    path("usage/<int:category_id>/", views.usage_list, name="usage-list"),
    path("usage/add/<int:category_id>/", views.usage_create, name="usage-create"),
    path("usage/", views.usage_overview, name="usage-overview"),  # View all categories + usage
]

