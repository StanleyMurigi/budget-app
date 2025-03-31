from django import forms
from .models import Budget, Category, Usage

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ["name", "amount", "start_date", "end_date"]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "end_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['budget', 'name', 'allocated_amount']
        widgets = {
            'budget': forms.Select(attrs={'class': 'form-control'}),
        }
        
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Get the logged-in user
        super().__init__(*args, **kwargs)
        if user:
            self.fields['budget'].queryset = Budget.objects.filter(user=user)  # Filter dropdown

class UsageForm(forms.ModelForm):
    class Meta:
        model = Usage
        fields = ['category', 'used_for', 'amount', 'discount']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'used_for': forms.TextInput(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'discount': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Get the logged-in user
        super().__init__(*args, **kwargs)
        if user:
            self.fields['category'].queryset = Category.objects.filter(user=user)  # Filter dropdown
