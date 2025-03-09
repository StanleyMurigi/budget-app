from rest_framework import generics, permissions
from .models import Budget, Category, BudgetAllocation, Usage
from .serializers import BudgetSerializer, CategorySerializer, BudgetAllocationSerializer

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

