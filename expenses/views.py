"""
Views for the Expense Tracker application.

This module contains all the view functions that handle:
- Displaying the expense list (dashboard)
- Adding new expenses
- Generating expense charts
- Making AI predictions
- Populating sample data
"""

import os
from datetime import datetime, timedelta
from decimal import Decimal
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Sum, Count
from django.db.models.functions import TruncDate
from django.conf import settings
from django.http import HttpResponse

from .models import Expense
from .forms import ExpenseForm
from .ml_predictor import ExpensePredictor, get_prediction_explanation

# Import Matplotlib for chart generation
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for server
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def expense_list(request):
    """
    Display the main dashboard with expense list and summary cards.
    
    This view shows:
    - Summary cards (total, this week, prediction)
    - List of all expenses (most recent first)
    """
    # Get all expenses
    expenses = Expense.objects.all()
    
    # Calculate totals for summary cards
    total_expenses = expenses.aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
    
    # This week's expenses
    today = datetime.now().date()
    week_start = today - timedelta(days=today.weekday())
    week_expenses = expenses.filter(date__gte=week_start).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
    
    # Get prediction for tomorrow
    predictor = ExpensePredictor()
    prediction_result = predictor.predict_next_day(expenses)
    predicted_amount = prediction_result.get('prediction', 0) if prediction_result.get('success') else None
    
    # Category breakdown
    category_totals = (
        expenses
        .values('category')
        .annotate(total=Sum('amount'), count=Count('id'))
        .order_by('-total')
    )
    
    context = {
        'expenses': expenses[:20],  # Show last 20 expenses
        'total_expenses': total_expenses,
        'week_expenses': week_expenses,
        'predicted_amount': predicted_amount,
        'category_totals': category_totals,
        'expense_count': expenses.count(),
    }
    
    return render(request, 'expense_list.html', context)


def expense_add(request):
    """
    Handle adding a new expense.
    
    GET: Display the expense form
    POST: Process the form and save the expense
    """
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save()
            messages.success(request, f'Expense of ₱{expense.amount} added successfully!')
            return redirect('expense_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        # Pre-fill with today's date
        form = ExpenseForm(initial={'date': datetime.now().date()})
    
    context = {
        'form': form,
        'title': 'Add New Expense',
    }
    
    return render(request, 'expense_add.html', context)


def expense_graph(request):
    """
    Generate and display expense charts.
    
    Creates:
    - Bar chart showing daily expenses for the last 7 days
    - Category breakdown summary
    """
    # Ensure chart directory exists
    chart_dir = settings.CHART_DIR
    os.makedirs(chart_dir, exist_ok=True)
    
    # Get expenses for the last 7 days
    today = datetime.now().date()
    week_ago = today - timedelta(days=6)
    
    # Get daily totals - using simple date field instead of TruncDate for SQLite compatibility
    daily_expenses = (
        Expense.objects
        .filter(date__gte=week_ago, date__lte=today)
        .values('date')
        .annotate(total=Sum('amount'))
        .order_by('date')
    )
    
    # Prepare data for all 7 days (including days with no expenses)
    date_totals = {d['date']: float(d['total']) for d in daily_expenses}
    
    dates = []
    amounts = []
    for i in range(7):
        date = week_ago + timedelta(days=i)
        dates.append(date)
        amounts.append(date_totals.get(date, 0))
    
    # Create the bar chart
    fig, ax = plt.subplots(figsize=(10, 5))
    
    # Style the chart
    colors = ['#6366F1' if amt > 0 else '#E2E8F0' for amt in amounts]
    bars = ax.bar(dates, amounts, color=colors, edgecolor='white', linewidth=1)
    
    # Customize the chart
    ax.set_xlabel('Date', fontsize=12, fontweight='bold', color='#1E293B')
    ax.set_ylabel('Amount (₱)', fontsize=12, fontweight='bold', color='#1E293B')
    ax.set_title('Daily Expenses - Last 7 Days', fontsize=14, fontweight='bold', color='#1E293B', pad=20)
    
    # Format x-axis dates
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
    ax.xaxis.set_major_locator(mdates.DayLocator())
    plt.xticks(rotation=45, ha='right')
    
    # Add value labels on bars
    for bar, amount in zip(bars, amounts):
        if amount > 0:
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 10,
                   f'₱{amount:,.0f}', ha='center', va='bottom', fontsize=9, color='#1E293B')
    
    # Style the chart background
    ax.set_facecolor('#F8FAFC')
    fig.patch.set_facecolor('#FFFFFF')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#E2E8F0')
    ax.spines['bottom'].set_color('#E2E8F0')
    ax.tick_params(colors='#64748B')
    ax.yaxis.grid(True, linestyle='--', alpha=0.3, color='#CBD5E1')
    
    plt.tight_layout()
    
    # Save the chart
    chart_path = os.path.join(chart_dir, 'daily_expenses.png')
    plt.savefig(chart_path, dpi=100, bbox_inches='tight', facecolor='white')
    plt.close()
    
    # Get category breakdown
    category_totals = (
        Expense.objects
        .filter(date__gte=week_ago, date__lte=today)
        .values('category')
        .annotate(total=Sum('amount'), count=Count('id'))
        .order_by('-total')
    )
    
    # Add emoji to categories
    category_data = []
    emoji_map = {'food': '🍔', 'transport': '🚗', 'bills': '💡', 'other': '📦'}
    name_map = {'food': 'Food', 'transport': 'Transport', 'bills': 'Bills', 'other': 'Other'}
    
    for cat in category_totals:
        category_data.append({
            'name': name_map.get(cat['category'], 'Other'),
            'emoji': emoji_map.get(cat['category'], '📦'),
            'total': cat['total'],
            'count': cat['count'],
        })
    
    # Calculate week total
    week_total = sum(amounts)
    
    context = {
        'chart_url': '/static/charts/daily_expenses.png',
        'category_data': category_data,
        'week_total': week_total,
        'date_range': f"{week_ago.strftime('%b %d')} - {today.strftime('%b %d, %Y')}",
    }
    
    return render(request, 'expense_graph.html', context)


def expense_prediction(request):
    """
    Display AI spending prediction.
    
    This view:
    - Trains/loads the ML model
    - Makes a prediction for tomorrow
    - Shows explanation of how it works
    """
    expenses = Expense.objects.all()
    predictor = ExpensePredictor()
    
    # Check if user wants to retrain
    if request.GET.get('retrain') == '1':
        result = predictor.train(expenses)
        if result.get('success'):
            messages.success(request, 'Model retrained successfully!')
        else:
            messages.warning(request, result.get('error', 'Could not train model'))
    else:
        result = predictor.predict_next_day(expenses)
    
    # Get model info
    model_info = predictor.get_model_info()
    
    # Get explanation
    explanation = get_prediction_explanation()
    
    # Calculate some stats
    expense_count = expenses.count()
    
    # Get date range of data
    if expense_count > 0:
        first_expense = expenses.order_by('date').first()
        last_expense = expenses.order_by('-date').first()
        date_range = f"{first_expense.date.strftime('%b %d')} - {last_expense.date.strftime('%b %d, %Y')}"
    else:
        date_range = "No data"
    
    context = {
        'prediction': result.get('prediction'),
        'success': result.get('success', False),
        'error': result.get('error'),
        'data_points': result.get('data_points', 0),
        'trend': result.get('trend'),
        'daily_change': result.get('daily_change'),
        'r2_score': result.get('r2_score'),
        'model_info': model_info,
        'explanation': explanation,
        'expense_count': expense_count,
        'date_range': date_range,
    }
    
    return render(request, 'expense_prediction.html', context)


def populate_sample_data(request):
    """
    Populate the database with sample expense data for demonstration.
    
    This creates realistic sample expenses over the past 30 days
    to demonstrate the system's features.
    """
    import random
    
    # Check if data already exists
    if Expense.objects.count() > 0:
        messages.warning(request, 'Sample data already exists. Clear existing data first if you want to repopulate.')
        return redirect('expense_list')
    
    # Sample data configuration
    categories = ['food', 'transport', 'bills', 'other']
    
    # Sample descriptions for each category
    descriptions = {
        'food': ['Lunch at restaurant', 'Grocery shopping', 'Coffee and snacks', 'Dinner delivery', 'Breakfast'],
        'transport': ['Grab ride', 'Gas/Fuel', 'Parking fee', 'Bus fare', 'Jeepney fare'],
        'bills': ['Electric bill', 'Water bill', 'Internet bill', 'Phone load', 'Subscription'],
        'other': ['Gift for friend', 'School supplies', 'Medicine', 'Household items', 'Entertainment'],
    }
    
    # Amount ranges for each category (in PHP)
    amount_ranges = {
        'food': (50, 500),
        'transport': (20, 300),
        'bills': (200, 2000),
        'other': (100, 1000),
    }
    
    # Generate expenses for the past 30 days
    today = datetime.now().date()
    expenses_created = 0
    
    for days_ago in range(30):
        date = today - timedelta(days=days_ago)
        
        # Random number of expenses per day (1-4)
        num_expenses = random.randint(1, 4)
        
        for _ in range(num_expenses):
            category = random.choice(categories)
            min_amt, max_amt = amount_ranges[category]
            amount = round(random.uniform(min_amt, max_amt), 2)
            description = random.choice(descriptions[category])
            
            Expense.objects.create(
                amount=Decimal(str(amount)),
                category=category,
                date=date,
                description=description
            )
            expenses_created += 1
    
    messages.success(request, f'Successfully created {expenses_created} sample expenses!')
    return redirect('expense_list')


def clear_data(request):
    """
    Clear all expense data from the database.
    
    This is useful for resetting the demo or starting fresh.
    """
    if request.method == 'POST':
        count = Expense.objects.count()
        Expense.objects.all().delete()
        
        # Also delete the ML model file
        if os.path.exists(settings.ML_MODEL_PATH):
            os.remove(settings.ML_MODEL_PATH)
        
        messages.success(request, f'Cleared {count} expenses and reset the ML model.')
        return redirect('expense_list')
    
    return render(request, 'confirm_clear.html')


def expense_delete(request, pk):
    """
    Delete a single expense.
    """
    try:
        expense = Expense.objects.get(pk=pk)
        amount = expense.amount
        expense.delete()
        messages.success(request, f'Expense of ₱{amount} deleted successfully!')
    except Expense.DoesNotExist:
        messages.error(request, 'Expense not found.')
    
    return redirect('expense_list')