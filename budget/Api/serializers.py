from .models import Budget, Category, BudgetAllocation, Gifts, Usage
from rest_framework import serializers

class UsageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Usage
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    """Serializer for user-defined expense categories."""
    usage = UsageSerializer(many=True, read_only=True)
    class Meta:
        model = Category
        fields = ['id', 'name', 'usage']

class BudgetAllocationSerializer(serializers.ModelSerializer):
    """Serializer for allocating budget amounts to categories."""
    
    category_name = serializers.ReadOnlyField(source="category.name")  # Readable category name

    class Meta:
        model = BudgetAllocation
        fields = ['id', 'category', 'category_name', 'allocated_amount']

class BudgetSerializer(serializers.ModelSerializer):
    """Serializer for budgets, including allocations."""
    
    allocations = BudgetAllocationSerializer(many=True, read_only=True)

    class Meta:
        model = Budget
        fields = ['id', 'name', 'amount', 'start_date', 'end_date', 'allocations']

class GiftSerializer(serializers.ModelSerializer):

    class Meta:
        model = Gifts
        fields = '__all__'
