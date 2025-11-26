"""
Expense Model - The core data structure for tracking expenses.

This model stores all expense records with:
- amount: How much money was spent
- category: What type of expense (Food, Transport, Bills, Other)
- date: When the expense occurred
- description: Optional notes about the expense
"""

from django.db import models
from django.utils import timezone


class Expense(models.Model):
    """
    Expense Model
    
    Represents a single expense entry in the system.
    Each expense has an amount, category, date, and optional description.
    """
    
    # Category choices - simple categories for easy classification
    CATEGORY_CHOICES = [
        ('food', '🍔 Food'),
        ('transport', '🚗 Transport'),
        ('bills', '💡 Bills'),
        ('other', '📦 Other'),
    ]
    
    # Amount field - stores the expense amount with 2 decimal places
    # max_digits=10 allows amounts up to 99,999,999.99
    amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        help_text="Amount spent in Philippine Peso (₱)"
    )
    
    # Category field - one of the predefined categories
    category = models.CharField(
        max_length=20, 
        choices=CATEGORY_CHOICES,
        default='other',
        help_text="Type of expense"
    )
    
    # Date field - when the expense occurred
    date = models.DateField(
        default=timezone.now,
        help_text="Date of the expense"
    )
    
    # Description field - optional notes about the expense
    description = models.TextField(
        blank=True,
        null=True,
        help_text="Optional description or notes"
    )
    
    # Timestamp for when the record was created
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Timestamp for when the record was last updated
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        """Meta options for the Expense model."""
        ordering = ['-date', '-created_at']  # Most recent first
        verbose_name = 'Expense'
        verbose_name_plural = 'Expenses'
    
    def __str__(self):
        """String representation of the expense."""
        return f"₱{self.amount} - {self.get_category_display()} on {self.date}"
    
    @property
    def category_emoji(self):
        """Return just the emoji for the category."""
        emoji_map = {
            'food': '🍔',
            'transport': '🚗',
            'bills': '💡',
            'other': '📦',
        }
        return emoji_map.get(self.category, '📦')
    
    @property
    def category_name(self):
        """Return just the name for the category (without emoji)."""
        name_map = {
            'food': 'Food',
            'transport': 'Transport',
            'bills': 'Bills',
            'other': 'Other',
        }
        return name_map.get(self.category, 'Other')