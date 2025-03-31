from rest_framework import generics, permissions
from .models import Budget, Category, BudgetAllocation, Usage
from .serializers import BudgetSerializer, CategorySerializer, BudgetAllocationSerializer
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from .models import Budget
from .forms import BudgetForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Budget, Category, Usage
from .forms import BudgetForm, CategoryForm, UsageForm
from django.contrib.auth.mixins import LoginRequiredMixin

@login_required
def index(request):
    return render(request, 'index.html')

@login_required
def manage_budgets(request):
    """View to manage budgets."""
    return render(request, 'budget/manage_budgets.html')




# Dashboard View
@login_required
def index(request):
    return render(request, 'index.html')

# Budgets CRUD
@login_required
def budget_list(request): 
    """View to display budgets for the logged-in user only."""
    budgets = Budget.objects.filter(user=request.user)  # Filter by logged-in user

    if not budgets.exists():
        pass
       

    return render(request, 'budget/manage_budgets.html', {'budgets': budgets})

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
def category_list(request, budget_id=None):
    """View to display budgets and their categories"""
    if budget_id:
        budget = get_object_or_404(Budget, id=budget_id, user=request.user)
        categories = Category.objects.filter(budget=budget, user=request.user)
        context = {"budget": budget, "categories": categories}
    else:
        budgets = Budget.objects.filter(user=request.user)
        categories = Category.objects.filter(budget__user=request.user, user=request.user)
        context = {"budgets": budgets, "categories": categories}

    return render(request, "budget/category_list.html", context)


@login_required
def category_create(request, budget_id):
    """Create a new category for a specific budget"""
    budget = get_object_or_404(Budget, id=budget_id, user=request.user)

    if request.method == "POST":
        form = CategoryForm(request.POST, user=request.user)
        if form.is_valid():
            category = form.save(commit=False)
            category.budget = budget  # Assign the selected budget
            category.user = request.user
            category.save()
            return redirect("category_list", budget_id=budget.id)  # Redirect to categories for this budget
    else:
        form = CategoryForm(user=request.user)

    return render(request, "budget/category_form.html", {"form": form, "budget": budget})

    
@login_required
def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk, user=request.user)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category, user=request.user)
    return render(request, 'budget/category_form.html', {'form': form})

@login_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk, user=request.user)
    if request.method == 'POST':
        category.delete()
        return redirect('category_list')
    return render(request, 'budget/category_delete.html', {'object': category})


@login_required
def usage_list(request, category_id):
    """Display all usage records under a category."""
    category = get_object_or_404(Category, id=category_id, user=request.user)
    usage_records = Usage.objects.filter(category=category, user=request.user)

    return render(request, "budget/usage_list.html", {"category": category, "usage_records": usage_records})


@login_required
def usage_create(request, category_id):
    """Add a new usage record to a category."""
    category = get_object_or_404(Category, id=category_id, user=request.user)

    if request.method == "POST":
        form = UsageForm(request.POST, user=request.user)
        if form.is_valid():
            usage = form.save(commit=False)
            usage.category = category
            usage.user = request.user  # Assign the logged-in user
            usage.save()
            return redirect("usage-list", category_id=category.id)

    else:
        form = UsageForm(user=request.user)

    return render(request, "budget/usage_form.html", {"form": form, "category": category})


@login_required
def usage_overview(request):
    """Show all categories and their usage records."""
    categories = Category.objects.filter(user=request.user).prefetch_related("usage")
    
    return render(request, "budget/usage_overview.html", {"categories": categories})

