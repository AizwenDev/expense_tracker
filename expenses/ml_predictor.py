"""
Machine Learning Predictor for Expense Tracking.

This module implements a simple Linear Regression model to predict
future spending based on historical expense data.

How it works (in simple terms):
1. We collect all past expenses and group them by date
2. We calculate the total spent each day
3. We use Linear Regression to find a pattern (trend line)
4. We use this pattern to predict tomorrow's spending

Linear Regression is like drawing a "best fit line" through your data points.
If your spending has been going up, the line will slope upward and predict
higher spending tomorrow.
"""

import os
from datetime import datetime, timedelta
from decimal import Decimal
import numpy as np
from django.conf import settings
from django.db.models import Sum
from django.db.models.functions import TruncDate

# Import ML libraries
try:
    from sklearn.linear_model import LinearRegression
    import joblib
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False
    print("Warning: scikit-learn not installed. ML features disabled.")


class ExpensePredictor:
    """
    A simple expense predictor using Linear Regression.
    
    This class:
    - Trains a model on historical expense data
    - Saves the trained model to a file (.joblib)
    - Loads the model to make predictions
    - Predicts tomorrow's expected spending
    """
    
    def __init__(self):
        """Initialize the predictor with the model path from settings."""
        self.model_path = getattr(settings, 'ML_MODEL_PATH', 'ml_model.joblib')
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """Load the trained model from file if it exists."""
        if not ML_AVAILABLE:
            return
            
        if os.path.exists(self.model_path):
            try:
                self.model = joblib.load(self.model_path)
            except Exception as e:
                print(f"Error loading model: {e}")
                self.model = None
    
    def _save_model(self):
        """Save the trained model to file."""
        if not ML_AVAILABLE or self.model is None:
            return
            
        try:
            joblib.dump(self.model, self.model_path)
        except Exception as e:
            print(f"Error saving model: {e}")
    
    def train(self, expenses_queryset):
        """
        Train the Linear Regression model on expense data.
        
        Args:
            expenses_queryset: Django QuerySet of Expense objects
            
        Returns:
            dict: Training results including success status and metrics
        """
        if not ML_AVAILABLE:
            return {
                'success': False,
                'error': 'Machine Learning libraries not installed',
                'prediction': None
            }
        
        # Group expenses by date and sum the amounts
        # Using simple values and grouping to avoid TruncDate issues with SQLite
        daily_totals = (
            expenses_queryset
            .values('date')
            .annotate(total=Sum('amount'))
            .order_by('date')
        )
        
        # Convert to list for processing
        data = [{'expense_date': d['date'], 'total': d['total']} for d in daily_totals]
        
        if len(data) < 2:
            return {
                'success': False,
                'error': 'Not enough data to train. Need at least 2 days of expenses.',
                'prediction': None,
                'data_points': len(data)
            }
        
        # Prepare training data
        # X = day number (1, 2, 3, ...)
        # y = total amount spent that day
        X = np.array(range(len(data))).reshape(-1, 1)
        y = np.array([float(d['total']) for d in data])
        
        # Create and train the model
        self.model = LinearRegression()
        self.model.fit(X, y)
        
        # Save the trained model
        self._save_model()
        
        # Calculate R² score (how well the model fits the data)
        r2_score = self.model.score(X, y)
        
        # Predict tomorrow (next day after the last data point)
        next_day = np.array([[len(data)]]).reshape(-1, 1)
        prediction = max(0, self.model.predict(next_day)[0])  # Can't be negative
        
        return {
            'success': True,
            'prediction': round(prediction, 2),
            'r2_score': round(r2_score, 4),
            'data_points': len(data),
            'trend': 'increasing' if self.model.coef_[0] > 0 else 'decreasing',
            'daily_change': round(float(self.model.coef_[0]), 2),
            'dates_range': {
                'start': data[0]['expense_date'],
                'end': data[-1]['expense_date']
            }
        }
    
    def predict_next_day(self, expenses_queryset):
        """
        Predict tomorrow's spending based on historical data.
        
        If no model exists, it will train one first.
        
        Args:
            expenses_queryset: Django QuerySet of Expense objects
            
        Returns:
            dict: Prediction results
        """
        # If no model exists, train one
        if self.model is None:
            return self.train(expenses_queryset)
        
        if not ML_AVAILABLE:
            return {
                'success': False,
                'error': 'Machine Learning libraries not installed',
                'prediction': None
            }
        
        # Get the number of days in the dataset
        daily_totals = (
            expenses_queryset
            .values('date')
            .annotate(total=Sum('amount'))
            .order_by('date')
        )
        
        data = [{'expense_date': d['date'], 'total': d['total']} for d in daily_totals]
        
        if len(data) < 1:
            return {
                'success': False,
                'error': 'No expense data available',
                'prediction': None
            }
        
        # Predict for the next day
        next_day = np.array([[len(data)]]).reshape(-1, 1)
        prediction = max(0, self.model.predict(next_day)[0])
        
        return {
            'success': True,
            'prediction': round(prediction, 2),
            'data_points': len(data),
            'model_loaded': True
        }
    
    def get_model_info(self):
        """
        Get information about the current model.
        
        Returns:
            dict: Model information
        """
        if not ML_AVAILABLE:
            return {
                'available': False,
                'reason': 'ML libraries not installed'
            }
        
        if self.model is None:
            return {
                'available': True,
                'trained': False,
                'reason': 'No model trained yet'
            }
        
        return {
            'available': True,
            'trained': True,
            'coefficient': round(float(self.model.coef_[0]), 4),
            'intercept': round(float(self.model.intercept_), 4),
            'model_path': str(self.model_path)
        }


def get_prediction_explanation():
    """
    Return a simple explanation of how the prediction works.
    
    This is useful for displaying to users who want to understand
    the AI prediction feature.
    """
    return {
        'title': 'How AI Prediction Works',
        'steps': [
            {
                'step': 1,
                'title': 'Collect Data',
                'description': 'We gather all your past expenses and group them by date.'
            },
            {
                'step': 2,
                'title': 'Calculate Daily Totals',
                'description': 'For each day, we add up all expenses to get a daily total.'
            },
            {
                'step': 3,
                'title': 'Find the Pattern',
                'description': 'Linear Regression draws a "best fit line" through your spending data.'
            },
            {
                'step': 4,
                'title': 'Make Prediction',
                'description': 'Using the pattern, we estimate what you might spend tomorrow.'
            }
        ],
        'note': 'This is a simple prediction based on trends. Actual spending may vary based on your real needs and circumstances.'
    }