"""
Django Admin configuration for the Expense model.

This allows managing expenses through Django's built-in admin interface.
"""

from django.contrib import admin
from .models import Expense


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    """Admin configuration for Expense model."""
    
    list_display = ('date', 'category', 'amount', 'description', 'created_at')
    list_filter = ('category', 'date')
    search_fields = ('description',)
    ordering = ('-date', '-created_at')
    date_hierarchy = 'date'
    
    fieldsets = (
        ('Expense Details', {
            'fields': ('amount', 'category', 'date', 'description')
        }),
    )