from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Budget(models.Model):
    """Model to store user's budget with categories and limits."""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="budgets")
    name = models.CharField(max_length=255)  # Budget name (e.g., "Monthly Budget")
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Total budget amount
    start_date = models.DateField()  # Budget start date
    end_date = models.DateField()  # Budget end date
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["user", "name"]

    def __str__(self):
        return f"{self.name} - {self.user.email}"


class Category(models.Model):
    """Model to store budget categories for expenses."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="categories")
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, related_name="categories")
    name = models.CharField(max_length=255)  # Category name (e.g., "Food", "Rent")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["user", "name"]

    def __str__(self):
        return f"{self.name} - {self.user.email}"


class BudgetAllocation(models.Model):
    """Model to allocate budget amounts to different categories."""

    #budget = models.ForeignKey(Budget, on_delete=models.CASCADE, related_name="allocations")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="allocations")
    allocated_amount = models.DecimalField(max_digits=10, decimal_places=2)  # Money allocated to this category
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.category.name}: {self.allocated_amount}"


class Usage(models.Model):
    """model for used amounts mapped to different categories"""
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="usage")
    used_for = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

class Gifts(models.Model):
    """model to store gifts and their value"""
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="gifts")
    gift_name = models.CharField(max_length=255)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
