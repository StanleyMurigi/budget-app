from rest_framework import generics, permissions
from ./models import Budget, Category, BudgetAllocation, Usage
from .serializers import BudgetSerializer, CategorySerializer, BudgetAllocationSerializer
from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from .models import Budget
from .forms import BudgetForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import BudgetForm, CategoryForm, UsageForm
from django.contrib.auth.mixins import LoginRequiredMixin

class BudgetListView(LoginRequiredMixin, ListView):
    """View for listing all budgets."""
    model = Budget
    template_name = "budget/list.html"
    context_object_name = "budgets"

    def get_queryset(self):
       return Budget.objects.filter(user=self.request.user).order_by('-start_date')
    
class BudgetCreateView(LoginRequiredMixin, CreateView):
    """View for creating a new budget."""
    model = Budget
    form_class = BudgetForm
    template_name = "budget/form.html"
    success_url = reverse_lazy("budget-list")

    def form_valid(self, form):
        form.instance.user = self.request.user  # Set the logged-in user
        return super().form_valid(form)

class CategoryListCreateView(generics.ListCreateAPIView):
    """View for listing and creating categories."""
    
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Return only the categories for the authenticated user."""
        return Category.objects.filter(user=self.request.user).prefetch_related('usage')

    def perform_create(self, serializer):
        """Save category for the current user."""
        serializer.save(user=self.request.user)

class BudgetListCreateView(generics.ListCreateAPIView):
    """View for listing and creating budgets."""
    
    serializer_class = BudgetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Return budgets only for the authenticated user."""
        return Budget.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Save budget for the current user."""
        serializer.save(user=self.request.user)

class BudgetDetailView(generics.RetrieveUpdateDestroyAPIView):
    """View for retrieving, updating, or deleting a budget."""
    
    serializer_class = BudgetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Ensure user can only access their own budgets."""
        return Budget.objects.filter(user=self.request.user)
