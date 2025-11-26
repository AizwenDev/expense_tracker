from django.apps import AppConfig


class ExpensesConfig(AppConfig):
    """Configuration for the Expenses application."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'expenses'
    verbose_name = 'Expense Tracker'