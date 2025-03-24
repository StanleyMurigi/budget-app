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
# @login_required
# def budget_list(request):
#     budgets = Budget.objects.filter(user=request.user)
#     return render(request, 'budget/list.html', {'budgets': budgets})

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
        categories = Category.objects.filter(budget=budget)
        context = {"budget": budget, "categories": categories}
    else:
        budgets = Budget.objects.filter(user=request.user)
        categories = Category.objects.filter(budget__user=request.user)
        context = {"budgets": budgets, "categories": categories}

    return render(request, "budget/category_list.html", context)


@login_required
def category_create(request, budget_id):
    """Create a new category for a specific budget"""
    budget = get_object_or_404(Budget, id=budget_id, user=request.user)

    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.budget = budget  # Assign the selected budget
            category.user = request.user
            category.save()
            return redirect("category_list", budget_id=budget.id)  # Redirect to categories for this budget
    else:
        form = CategoryForm()

    return render(request, "budget/category_form.html", {"form": form, "budget": budget})

    
@login_required
def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk, user=request.user)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'budget/category_form.html', {'form': form})

@login_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk, user=request.user)
    if request.method == 'POST':
        category.delete()
        return redirect('category_list')
    return render(request, 'budget/category_confirm_delete.html', {'object': category})


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
        form = UsageForm(request.POST)
        if form.is_valid():
            usage = form.save(commit=False)
            usage.category = category
            usage.user = request.user  # Assign the logged-in user
            usage.save()
            return redirect("usage-list", category_id=category.id)

    else:
        form = UsageForm()

    return render(request, "budget/usage_form.html", {"form": form, "category": category})


@login_required
def usage_overview(request):
    """Show all categories and their usage records."""
    categories = Category.objects.filter(user=request.user).prefetch_related("usage")
    
    return render(request, "budget/usage_overview.html", {"categories": categories})


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

