from flask import Flask, render_template, jsonify, request, redirect, session
import numpy as np
import mysql.connector
import google.generativeai as genai
import os
from main import predicts  

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Needed for session storage

# Database Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",  # Change this
    password="Vicky5629",  # Change this
    database="finance_app"
)
cursor = db.cursor()

# Ensure tables exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255) NOT NULL,
        email VARCHAR(255) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL
    )
""")
db.commit()

# Set your Gemini AI API Key
GEMINI_API_KEY = "AIzaSyC53kq90Sk0QTuUAbNjJWXSDxk_2s_z6uk"  # Replace with your actual API key
genai.configure(api_key=GEMINI_API_KEY)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user_email' not in session:
        return redirect('/login')  # Redirect if not logged in

    if request.method == 'POST':
        data = request.json
        return {"selected": data['selected']}
    
    return render_template('dashboard.html')

# ----------------- Owned Expenses -----------------
@app.route("/submit_owned", methods=["POST"])
def submit_owned():
    # Get form data
    income = float(request.form.get("income", 0))
    property_tax = float(request.form.get("propertyTax", 0))
    electricity = float(request.form.get("electricity", 0))
    food = float(request.form.get("food", 0))
    maintenance = float(request.form.get("maintenance", 0))
    internet = float(request.form.get("internet", 0))
    transport = float(request.form.get("transport", 0))
    personal_care = float(request.form.get("personalCare", 0))
    miscellaneous = float(request.form.get("miscellaneous", 0))

    # Calculate total expenses
    total_expenses = (
        property_tax + electricity + food + maintenance + internet + 
        transport + personal_care + miscellaneous
    )

    # Store data in session
    session["income"] = income
    session["expenses"] = total_expenses

    # Redirect to owned_category.html
    return redirect("/owned_category")

@app.route("/owned_category")
def owned_category():
    income = session.get("income", 1)  # Default to 1 to prevent division by zero
    expenses = session.get("expenses", 0)

    # Classify spender
    percentage = (expenses / income) * 100
    if percentage <= 30:
        spender_category = "Low Spender"
    elif percentage <= 70:
        spender_category = "Medium Spender"
    else:
        spender_category = "High Spender"
    

    return render_template("owned_category.html", spender_category=spender_category)

# ----------------- Rented House Expenses -----------------
@app.route("/submit_rented", methods=["POST"])
def submit_rented():
    # Get form data
    income = float(request.form.get("income", 0))
    rent_amount = float(request.form.get("rent", 0))
    internet = float(request.form.get("internet", 0))
    insurance = float(request.form.get("insurance", 0))
    food = float(request.form.get("food", 0))
    electricity = float(request.form.get("electricity", 0))
    personal_care = float(request.form.get("personalCare", 0))
    maintenance = float(request.form.get("maintenance", 0))
    transport = float(request.form.get("transport", 0))
    misc = float(request.form.get("miscellaneous", 0))

    # Calculate total expenses
    total_expenses = (
        rent_amount + internet + insurance + food + electricity + 
        maintenance + transport + misc + personal_care
    )

    # Store in session
    session["income_rented"] = income
    session["expenses_rented"] = total_expenses

    return redirect("/rented_category")

@app.route("/rented_category")
def rented_category():
    income = session.get("income_rented", 1)  # Prevent division by zero
    expenses = session.get("expenses_rented", 0)

    # Classify spender
    percentage = (expenses / income) * 100
    if percentage <= 30:
        spender_category = "Low Spender"
    elif percentage <= 70:
        spender_category = "Medium Spender"
    else:
        spender_category = "High Spender"

    return render_template("rented_category.html", spender_category=spender_category)


# ----------------- General Expenses -----------------
@app.route("/submit_general", methods=["POST"])
def submit_general():
    # Get form data
    income = float(request.form.get("income", 0))
    internet_mobile = float(request.form.get("internet", 0))
    groceries = float(request.form.get("groceries", 0))
    entertainment = float(request.form.get("entertainment", 0))
    transportation = float(request.form.get("transportation", 0))
    shopping = float(request.form.get("shopping", 0))
    medical = float(request.form.get("medical", 0))
    subscriptions = float(request.form.get("subscriptions", 0))
    misc = float(request.form.get("miscellaneous", 0))

    # Calculate total expenses
    total_expenses = (
        internet_mobile + groceries + entertainment + transportation + shopping +
        medical + subscriptions + misc
    )

    # Store in session (Force update)
    session["income_general"] = income
    session["expenses_general"] = total_expenses
    session.modified = True  # ✅ Ensure session updates

    print(f"✅ General Expenses Stored: {session['expenses_general']}")
    print(f"✅ General Income Stored: {session['income_general']}")

    return redirect("/general_category")

@app.route("/general_category")
def general_category():
    income = session.get("income_general", 1)
    expenses = session.get("expenses_general", 0)

    # Classify spender
    percentage = (expenses / income) * 100
    if percentage <= 30:
        spender_category = "Low Spender"
    elif percentage <= 70:
        spender_category = "Medium Spender"
    else:
        spender_category = "High Spender"

    return render_template("general_category.html", spender_category=spender_category)

@app.route('/form_owned')
def form_owned():
    return render_template('form_owned.html')

@app.route('/form_rented')
def form_rented():
    return render_template('form_rented.html')

@app.route('/form_general')
def form_general():
    return render_template('form_general.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
        res = cursor.fetchone()

        if res:
            session['user_email'] = email  # Store user session
            return redirect('/dashboard')  # Redirect to dashboard
        else:
            return render_template('login.html', message='Invalid email or password.')
    return render_template('login.html', message='')

@app.route('/logout')
def logout():
    session.pop('user_email', None)  # Clear user session
    return redirect('/login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Check if email already exists
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        if cursor.fetchone():
            return render_template('register.html', message="Email already registered. Please log in.")

        try:
            cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", 
                           (username, email, password))
            db.commit()
            return redirect('/login')
        except Exception as e:
            return str(e)
    return render_template('register.html')

@app.route('/submit-form', methods=['POST'])
def submit_form():
    try:
        expense = request.form.get('expense')  # Get data from form
        if expense:
            if 'expense_data' not in session:
                session['expense_data'] = []
            session['expense_data'].append(float(expense))
        
        return redirect('/visualization')  # Redirect to visualization page
    except ValueError:
        return "Invalid input, please enter a valid number.", 400


@app.route("/overview")
def overview():
    return render_template("overview.html")

@app.route("/get_advice", methods=["POST"])
def fetch_advice():
    """API endpoint to provide financial advice based on spending category."""
    data = request.get_json()
    category = data.get("category", "Medium Spender")  # Default category

    # Debugging logs (check Flask logs)
    print(f"Category: {category}")

    # Define AI Prompt based on category
    prompt = f"""
    You are a financial expert giving friendly and practical money advice.  
    The user is a '{category}' spender.  

    Speak in a natural, conversational tone, like a friend giving useful tips.  
    Keep the response short (2 to 3 lines) and easy to understand.  
    Use rupees instead of dollars and avoid complex financial jargon.  

    Examples:  

    For a Low Spender:  
    "You're managing your expenses well. Start investing in low-risk mutual funds or bonds to grow your savings. Try to save at least 10% of your income for emergencies."  

    For a Medium Spender:  
    "You're balancing spending and savings. Cut down on non-essential expenses by 15% and consider investing in index funds for long-term growth."  

    For a High Spender:  
    "You're spending a lot. Set a monthly budget and track your extra expenses. Try automating savings and investing in SIPs to build wealth over time."  

    Now, provide advice in the same style based on the user’s category.
    """

    # Call AI model for advice
    model = genai.GenerativeModel('gemini-2.0-flash')
    response = model.generate_content(prompt)

    return jsonify({"advice": response.text})

if __name__ == '__main__':
    app.run(debug=True)