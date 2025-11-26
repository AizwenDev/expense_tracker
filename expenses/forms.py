"""
Forms for the Expense Tracker application.

This module contains Django forms for user input validation and rendering.
"""

from django import forms
from .models import Expense


class ExpenseForm(forms.ModelForm):
    """
    Form for creating and editing expenses.
    
    This form is based on the Expense model and provides:
    - Input validation
    - HTML widget customization
    - User-friendly labels and placeholders
    """
    
    class Meta:
        model = Expense
        fields = ['amount', 'category', 'date', 'description']
        
        # Custom widgets for better UI
        widgets = {
            'amount': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0.01',
                'required': True,
            }),
            'category': forms.Select(attrs={
                'class': 'form-select',
                'required': True,
            }),
            'date': forms.DateInput(attrs={
                'class': 'form-input',
                'type': 'date',
                'required': True,
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Optional: Add notes about this expense...',
                'rows': 3,
            }),
        }
        
        # Custom labels
        labels = {
            'amount': 'Amount (₱)',
            'category': 'Category',
            'date': 'Date',
            'description': 'Description (Optional)',
        }
        
        # Help text
        help_texts = {
            'amount': 'Enter the amount spent',
            'category': 'Select the type of expense',
            'date': 'When did you make this expense?',
            'description': 'Add any notes or details',
        }
    
    def clean_amount(self):
        """Validate that amount is positive."""
        amount = self.cleaned_data.get('amount')
        if amount is not None and amount <= 0:
            raise forms.ValidationError('Amount must be greater than zero.')
        return amount