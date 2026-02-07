"""
Flask Web Application for Lunch Offer Menu - WITH DATABASE
This version saves orders to a PostgreSQL database
"""

from flask import Flask, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import secrets
import os

# Create Flask application
app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# DATABASE CONFIGURATION
# For production (Render), use PostgreSQL from environment variable
# For local development, use SQLite (simpler)
if os.environ.get('DATABASE_URL'):
    # Render provides DATABASE_URL, but we need to fix the protocol
    database_url = os.environ.get('DATABASE_URL')
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
else:
    # Local SQLite database for testing
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///orders.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

# DATABASE MODEL - defines what we store
class Order(db.Model):
    """
    This represents an order in the database
    Each order has: id, items selected, prices, total, and timestamp
    """
    id = db.Column(db.Integer, primary_key=True)
    sandwich = db.Column(db.String(100), nullable=False)
    crisps = db.Column(db.String(100), nullable=False)
    snack = db.Column(db.String(100), nullable=False)
    sandwich_price = db.Column(db.Float, nullable=False)
    crisps_price = db.Column(db.Float, nullable=False)
    snack_price = db.Column(db.Float, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    offer_applied = db.Column(db.Boolean, nullable=False)
    savings = db.Column(db.Float, default=0.0)
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Order {self.id}: {self.sandwich}>'


# Menu data (same as before)
sandwiches = {
    "Ham & Cheese": 3.50,
    "Tuna Mayo": 3.50,
    "Chicken Salad": 3.50,
    "BLT": 3.50,
    "Egg Mayo": 3.50,
    "Cheese & Pickle": 3.50,
    "Prawn Mayo": 4.50,
    "Steak & Onion": 4.50
}

crisps = {
    "Ready Salted": 1.50,
    "Salt & Vinegar": 1.50,
    "Cheese & Onion": 1.50,
    "Prawn Cocktail": 1.50,
    "BBQ": 1.50,
    "Sour Cream": 1.50,
    "Paprika": 1.50,
    "Spicy Chili": 1.50
}

snacks = {
    "Apple": 1.00,
    "Banana": 1.00,
    "Chocolate Bar": 2.00,
    "Granola Bar": 2.00,
    "Cookie": 1.50,
    "Brownie": 2.00,
    "Fruit Pot": 2.50,
    "Yogurt": 2.00
}

premium_sandwiches = ["Prawn Mayo", "Steak & Onion"]
lunch_offer_price = 5.00


def check_offer_eligibility(sandwich_choice):
    """Check if the selected items qualify for the lunch offer"""
    return sandwich_choice not in premium_sandwiches


def calculate_total(sandwich, crisp, snack, qualifies_for_offer):
    """Calculate the total price"""
    if qualifies_for_offer:
        return lunch_offer_price
    else:
        total = sandwiches[sandwich] + crisps[crisp] + snacks[snack]
        return total


# ROUTES
@app.route('/')
def index():
    """Home page - display the menu selection form"""
    return render_template('index.html', 
                         sandwiches=sandwiches,
                         crisps=crisps,
                         snacks=snacks,
                         premium_sandwiches=premium_sandwiches)


@app.route('/calculate', methods=['POST'])
def calculate():
    """Process the form submission, save to database, and show results"""
    # Get the selected items from the form
    sandwich_choice = request.form.get('sandwich')
    crisp_choice = request.form.get('crisp')
    snack_choice = request.form.get('snack')
    
    # Check if all items were selected
    if not sandwich_choice or not crisp_choice or not snack_choice:
        return render_template('index.html',
                             sandwiches=sandwiches,
                             crisps=crisps,
                             snacks=snacks,
                             premium_sandwiches=premium_sandwiches,
                             error="Please select one item from each category")
    
    # Calculate results
    qualifies = check_offer_eligibility(sandwich_choice)
    total = calculate_total(sandwich_choice, crisp_choice, snack_choice, qualifies)
    
    # Calculate savings
    savings = 0
    if qualifies:
        regular_total = sandwiches[sandwich_choice] + crisps[crisp_choice] + snacks[snack_choice]
        savings = regular_total - total
    
    # SAVE ORDER TO DATABASE
    new_order = Order(
        sandwich=sandwich_choice,
        crisps=crisp_choice,
        snack=snack_choice,
        sandwich_price=sandwiches[sandwich_choice],
        crisps_price=crisps[crisp_choice],
        snack_price=snacks[snack_choice],
        total_price=total,
        offer_applied=qualifies,
        savings=savings
    )
    
    db.session.add(new_order)  # Add to database session
    db.session.commit()  # Save to database
    
    # Show results page
    return render_template('result.html',
                         sandwich=sandwich_choice,
                         crisp=crisp_choice,
                         snack=snack_choice,
                         qualifies=qualifies,
                         total=total,
                         savings=savings,
                         sandwich_price=sandwiches[sandwich_choice],
                         crisp_price=crisps[crisp_choice],
                         snack_price=snacks[snack_choice],
                         order_id=new_order.id)


@app.route('/history')
def history():
    """Display all past orders from the database"""
    # Query all orders, newest first
    all_orders = Order.query.order_by(Order.order_date.desc()).all()
    
    # Calculate statistics
    total_orders = len(all_orders)
    total_revenue = sum(order.total_price for order in all_orders)
    total_savings = sum(order.savings for order in all_orders)
    offers_applied = sum(1 for order in all_orders if order.offer_applied)
    
    return render_template('history.html',
                         orders=all_orders,
                         total_orders=total_orders,
                         total_revenue=total_revenue,
                         total_savings=total_savings,
                         offers_applied=offers_applied)


# Create database tables
with app.app_context():
    db.create_all()  # Creates tables if they don't exist


# Run the application
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=True, host='0.0.0.0', port=port)