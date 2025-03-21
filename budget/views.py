from rest_framework import generics, permissions
from .models import Budget, Category, BudgetAllocation, Usage
from .serializers import BudgetSerializer, CategorySerializer, BudgetAllocationSerializer
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

@login_required
def index(request):
    return render(request, 'index.html')

@login_required
def manage_budgets(request):
    """View to manage budgets."""
    return render(request, 'budget/manage_budgets.html')


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Budget, Category, Usage
from .forms import BudgetForm, CategoryForm, UsageForm

# Dashboard View
@login_required
def index(request):
    return render(request, 'index.html')

# Budgets CRUD
@login_required
def budget_list(request):
    budgets = Budget.objects.filter(user=request.user)
    return render(request, 'budget/list.html', {'budgets': budgets})

@login_required
def budget_create(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            budget.save()
            return redirect('budget-list')
    else:
        form = BudgetForm()
    return render(request, 'budget/form.html', {'form': form})

@login_required
def budget_update(request, pk):
    budget = get_object_or_404(Budget, pk=pk, user=request.user)
    if request.method == 'POST':
        form = BudgetForm(request.POST, instance=budget)
        if form.is_valid():
            form.save()
            return redirect('budget-list')
    else:
        form = BudgetForm(instance=budget)
    return render(request, 'budget/form.html', {'form': form})

@login_required
def budget_delete(request, pk):
    budget = get_object_or_404(Budget, pk=pk, user=request.user)
    if request.method == 'POST':
        budget.delete()
        return redirect('budget-list')
    return render(request, 'budget/confirm_delete.html', {'object': budget})

# Similarly, implement CRUD for Categories
@login_required
def category_list(request):
    categories = Category.objects.filter(user=request.user)
    return render(request, 'category/list.html', {'categories': categories})

@login_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            return redirect('category-list')
    else:
        form = CategoryForm()
    return render(request, 'category/form.html', {'form': form})

@login_required
def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk, user=request.user)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category-list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'category/form.html', {'form': form})

@login_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk, user=request.user)
    if request.method == 'POST':
        category.delete()
        return redirect('category-list')
    return render(request, 'category/confirm_delete.html', {'object': category})


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

