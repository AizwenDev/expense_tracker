# 💰 Expense Tracker with AI Spending Prediction

A complete, portable Django-based expense tracking system with Machine Learning prediction capabilities. Perfect for students learning web development and basic ML concepts.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Django](https://img.shields.io/badge/Django-4.2-green.svg)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey.svg)
![ML](https://img.shields.io/badge/ML-Scikit--learn-orange.svg)

---

## 📋 Table of Contents

1. [What is This Project?](#-what-is-this-project)
2. [Features](#-features)
3. [Project Structure](#-project-structure)
4. [How to Run](#-how-to-run)
5. [How Django Works](#-how-django-works)
6. [How the ML Prediction Works](#-how-the-ml-prediction-works)
7. [Running from USB](#-running-from-usb)
8. [For the Panel](#-for-the-panel)
9. [Technical Details](#-technical-details)
10. [Troubleshooting](#-troubleshooting)

---

## 🎯 What is This Project?

This is an **Expense Tracker** - a web application that helps you:
- Record your daily expenses
- Categorize spending (Food, Transport, Bills, Other)
- View spending charts and graphs
- **Predict tomorrow's spending using AI (Machine Learning)**

### Why is it Special?
- **Portable**: Runs from a USB flash drive - no installation needed!
- **Simple**: Easy to understand code for learning
- **Complete**: Includes database, web interface, charts, and ML
- **Beginner-Friendly**: Well-commented code with explanations

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 📝 **Add Expenses** | Record amount, category, date, and description |
| 📋 **View Expenses** | See all expenses in a beautiful dashboard |
| 📊 **Charts** | Visual bar chart of daily spending (last 7 days) |
| 🔮 **AI Prediction** | Machine Learning predicts tomorrow's spending |
| 📥 **Sample Data** | One-click to load demo data |
| 🗑️ **Delete** | Remove individual expenses or clear all data |
| 💾 **Portable** | SQLite database stays with the project |

---

## 📁 Project Structure

```
expense_tracker/
│
├── 📄 run.bat                    # Double-click to run (Windows)
├── 📄 requirements.txt           # Python dependencies
├── 📄 README.md                  # This documentation
├── 📄 manage.py                  # Django management script
├── 📄 db.sqlite3                 # Database (auto-created)
├── 📄 ml_model.joblib            # ML model (auto-created)
│
├── 📁 expense_tracker/           # Django project settings
│   ├── __init__.py
│   ├── settings.py               # Configuration
│   ├── urls.py                   # Main URL routing
│   └── wsgi.py                   # Web server interface
│
├── 📁 expenses/                  # Main application
│   ├── __init__.py
│   ├── models.py                 # Expense data model
│   ├── views.py                  # Page logic
│   ├── urls.py                   # App URL routing
│   ├── forms.py                  # Input forms
│   ├── ml_predictor.py           # ML prediction code
│   ├── admin.py                  # Admin interface
│   └── apps.py                   # App configuration
│
├── 📁 templates/                 # HTML templates
│   ├── base.html                 # Base template with CSS
│   ├── expense_list.html         # Dashboard page
│   ├── expense_add.html          # Add expense form
│   ├── expense_graph.html        # Charts page
│   ├── expense_prediction.html   # AI prediction page
│   └── confirm_clear.html        # Delete confirmation
│
└── 📁 static/                    # Static files
    └── 📁 charts/                # Generated chart images
```

---

## 🚀 How to Run

### Option 1: Double-Click (Easiest)
1. Make sure Python is installed on your computer
2. Double-click `run.bat`
3. Wait for the browser to open
4. Start tracking expenses!

### Option 2: Manual Steps
```bash
# 1. Open terminal in the project folder

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run database migrations
python manage.py migrate

# 6. Start the server
python manage.py runserver

# 7. Open browser to http://127.0.0.1:8000
```

---

## 🌐 How Django Works

Django is a **web framework** - it helps you build websites quickly. Here's how it works in simple terms:

### The MTV Pattern (Model-Template-View)

```
┌─────────────────────────────────────────────────────────────┐
│                     USER'S BROWSER                          │
│                    (Chrome, Firefox)                        │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      DJANGO SERVER                          │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                    URLs (urls.py)                    │   │
│  │         "Which page did the user request?"           │   │
│  └─────────────────────────────────────────────────────┘   │
│                            │                                │
│                            ▼                                │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                   VIEWS (views.py)                   │   │
│  │         "What should we show the user?"              │   │
│  │         - Get data from database                     │   │
│  │         - Process the request                        │   │
│  │         - Prepare the response                       │   │
│  └─────────────────────────────────────────────────────┘   │
│              │                           │                  │
│              ▼                           ▼                  │
│  ┌──────────────────────┐   ┌──────────────────────────┐   │
│  │   MODELS (models.py) │   │  TEMPLATES (.html files) │   │
│  │   "What data do we   │   │  "How should it look?"   │   │
│  │    have?"            │   │  - HTML structure        │   │
│  │   - Expense amount   │   │  - CSS styling           │   │
│  │   - Category         │   │  - Display data          │   │
│  │   - Date             │   │                          │   │
│  └──────────────────────┘   └──────────────────────────┘   │
│              │                                              │
│              ▼                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              DATABASE (db.sqlite3)                   │   │
│  │              Stores all expense data                 │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### Step-by-Step Flow

1. **User visits a page** (e.g., http://127.0.0.1:8000/add/)

2. **URLs.py checks the address**
   - "Oh, /add/ means the user wants to add an expense"
   - "Let me call the `expense_add` view"

3. **Views.py handles the request**
   - If GET request: "Show the empty form"
   - If POST request: "Save the new expense to database"

4. **Models.py defines the data**
   - "An Expense has: amount, category, date, description"
   - Django automatically creates database tables

5. **Templates render the HTML**
   - "Here's the form with nice styling"
   - "Insert the data from the view"

6. **Response sent to browser**
   - User sees the beautiful page!

---

## 🤖 How the ML Prediction Works

### What is Machine Learning?

Machine Learning is teaching computers to find patterns in data and make predictions. Our system uses **Linear Regression** - one of the simplest ML algorithms.

### Linear Regression Explained

Imagine you're plotting your daily spending on a graph:

```
Amount (₱)
    │
800 │                    ●
    │              ●
600 │        ●
    │  ●
400 │
    │
200 │
    │
  0 └────────────────────────
    Day 1  Day 2  Day 3  Day 4
```

Linear Regression draws the **"best fit line"** through these points:

```
Amount (₱)
    │
800 │                    ●  ─────── Predicted
    │              ●   ─────        Day 5!
600 │        ● ─────
    │  ● ─────
400 │─────
    │
200 │
    │
  0 └────────────────────────────
    Day 1  Day 2  Day 3  Day 4  Day 5
```

### The Math (Simple Version)

The formula is: **y = mx + b**

- **y** = predicted spending (what we want to find)
- **m** = slope (how much spending changes per day)
- **x** = day number
- **b** = starting point

### Our ML Pipeline

```
┌─────────────────────────────────────────────────────────────┐
│                    ML PREDICTION PIPELINE                    │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 1: COLLECT DATA                                       │
│  Get all expenses from database                             │
│  Example: [(Day 1, ₱500), (Day 2, ₱300), (Day 3, ₱700)]    │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 2: GROUP BY DATE                                      │
│  Add up all expenses for each day                           │
│  Example: Day 1 total = ₱500, Day 2 total = ₱300           │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 3: PREPARE TRAINING DATA                              │
│  X = [1, 2, 3, ...]  (day numbers)                         │
│  y = [500, 300, 700, ...]  (daily totals)                  │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 4: TRAIN THE MODEL                                    │
│  LinearRegression().fit(X, y)                               │
│  Finds the best line through the data points                │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 5: SAVE THE MODEL                                     │
│  joblib.dump(model, 'ml_model.joblib')                     │
│  Save so we don't have to retrain every time               │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 6: MAKE PREDICTION                                    │
│  model.predict([[next_day_number]])                         │
│  "Based on the pattern, tomorrow you'll spend ₱X"          │
└─────────────────────────────────────────────────────────────┘
```

### Code Walkthrough

```python
# From ml_predictor.py

# Step 1-2: Get daily totals from database
daily_totals = Expense.objects.annotate(
    expense_date=TruncDate('date')
).values('expense_date').annotate(
    total=Sum('amount')
)

# Step 3: Prepare data
X = np.array(range(len(data))).reshape(-1, 1)  # Day numbers
y = np.array([d['total'] for d in data])        # Daily totals

# Step 4: Train the model
model = LinearRegression()
model.fit(X, y)

# Step 5: Save the model
joblib.dump(model, 'ml_model.joblib')

# Step 6: Predict tomorrow
next_day = len(data)  # Tomorrow's day number
prediction = model.predict([[next_day]])[0]
```

---

## 💾 Running from USB

### Why Portable?

- **No installation** on the host computer
- **Carry your data** with you
- **Demo anywhere** without setup
- **Perfect for presentations**

### How It Works

1. **SQLite Database**: Unlike MySQL or PostgreSQL, SQLite stores everything in a single file (`db.sqlite3`). This file stays in your project folder.

2. **Virtual Environment**: The `venv` folder contains all Python packages. Once created, it works offline.

3. **No External Services**: Everything runs locally - no internet needed after setup.

### USB Setup Steps

1. Copy the entire `expense_tracker` folder to your USB drive
2. On any Windows computer with Python installed:
   - Navigate to the folder on USB
   - Double-click `run.bat`
   - Wait for setup (first time takes longer)
   - Browser opens automatically!

### Requirements for Host Computer

- Python 3.8 or higher installed
- Python added to system PATH
- About 500MB free space (for virtual environment)

---

## 🎓 For the Panel

### Key Talking Points

1. **Architecture**
   - "This is a Django web application following the MTV pattern"
   - "Data is stored in SQLite for portability"
   - "The ML model uses scikit-learn's Linear Regression"

2. **Technologies Used**
   | Technology | Purpose |
   |------------|---------|
   | Django 4.2 | Web framework |
   | SQLite | Database |
   | Matplotlib | Chart generation |
   | Scikit-learn | Machine Learning |
   | Joblib | Model persistence |
   | HTML/CSS | User interface |

3. **ML Explanation**
   - "We use Linear Regression to find spending trends"
   - "The model learns from historical data"
   - "It predicts by extending the trend line"

4. **Portability**
   - "The entire system runs from a single folder"
   - "No database server needed - SQLite is file-based"
   - "Can run from USB on any computer with Python"

### Possible Questions & Answers

**Q: Why Linear Regression?**
A: It's simple, interpretable, and works well for trend prediction. More complex models would be overkill for this use case.

**Q: How accurate is the prediction?**
A: The R² score shows model fit. Real accuracy depends on spending consistency. It's meant to show trends, not exact amounts.

**Q: Why Django instead of Flask?**
A: Django provides more built-in features (ORM, admin, forms) making it faster to develop a complete application.

**Q: Why SQLite?**
A: SQLite is file-based, requiring no server setup. Perfect for portable applications and learning.

**Q: Can this scale to many users?**
A: For production, you'd switch to PostgreSQL and add user authentication. This demo focuses on core concepts.

---

## ⚙️ Technical Details

### Dependencies

```
Django>=4.2,<5.0      # Web framework
matplotlib>=3.7.0      # Chart generation
scikit-learn>=1.3.0    # Machine Learning
joblib>=1.3.0          # Model saving/loading
numpy>=1.24.0          # Numerical operations
```

### Database Schema

```sql
CREATE TABLE expenses_expense (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount DECIMAL(10, 2) NOT NULL,
    category VARCHAR(20) NOT NULL,
    date DATE NOT NULL,
    description TEXT,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL
);
```

### URL Routes

| URL | View | Description |
|-----|------|-------------|
| `/` | expense_list | Dashboard |
| `/add/` | expense_add | Add expense form |
| `/graph/` | expense_graph | Charts page |
| `/predict/` | expense_prediction | AI prediction |
| `/sample/` | populate_sample_data | Load demo data |
| `/clear/` | clear_data | Delete all data |
| `/delete/<id>/` | expense_delete | Delete one expense |

---

## 🔧 Troubleshooting

### "Python is not recognized"
- Install Python from https://python.org
- Check "Add Python to PATH" during installation
- Restart your terminal/command prompt

### "Module not found" errors
```bash
pip install -r requirements.txt
```

### "Database is locked"
- Close any other programs using the database
- Make sure only one server instance is running

### Charts not showing
- Check that `static/charts/` folder exists
- Refresh the page after viewing graph

### Prediction shows error
- Need at least 2 days of expense data
- Click "Load Sample Data" for demo

---

## 📝 License

This project is created for educational purposes. Feel free to use, modify, and learn from it!

---

## 👨‍💻 Created By

**Expense Tracker with AI Prediction**
A Django + Machine Learning demonstration project

Built with ❤️ for learning