"""
URL configuration for the expenses app.

This module defines all the URL patterns for the expense tracker:
- / : Home page (expense list/dashboard)
- /add/ : Add new expense
- /graph/ : View expense charts
- /predict/ : AI spending prediction
- /sample/ : Populate sample data
- /clear/ : Clear all data
- /delete/<id>/ : Delete single expense
"""

from django.urls import path
from . import views

urlpatterns = [
    # Main dashboard - list all expenses
    path('', views.expense_list, name='expense_list'),
    
    # Add new expense
    path('add/', views.expense_add, name='expense_add'),
    
    # View expense graph/chart
    path('graph/', views.expense_graph, name='expense_graph'),
    
    # AI prediction page
    path('predict/', views.expense_prediction, name='expense_prediction'),
    
    # Populate sample data (for demo)
    path('sample/', views.populate_sample_data, name='populate_sample'),
    
    # Clear all data
    path('clear/', views.clear_data, name='clear_data'),
    
    # Delete single expense
    path('delete/<int:pk>/', views.expense_delete, name='expense_delete'),
]