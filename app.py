"""
Flask Web Application for Lunch Offer Menu - WITH DATABASE AND ADMIN PANEL
This version includes an admin panel to manage menu items
"""

from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from functools import wraps
import secrets
import os

# Create Flask application
app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# ADMIN PASSWORD - Change this to your own secure password!
# In production, you should use environment variables
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'Sandwich123')

# DATABASE CONFIGURATION
if os.environ.get('DATABASE_URL'):
    database_url = os.environ.get('DATABASE_URL')
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql+pg8000://', 1)
    elif database_url.startswith('postgresql://'):
        database_url = database_url.replace('postgresql://', 'postgresql+pg8000://', 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///orders.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

# DATABASE MODELS
class Order(db.Model):
    """Stores customer orders"""
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


class MenuItem(db.Model):
    """Stores menu items that can be managed by admin"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)  # sandwich, crisps, snack
    is_premium = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<MenuItem {self.name}>'


# HELPER FUNCTIONS
def get_menu_items():
    """Get active menu items organized by category"""
    items = MenuItem.query.filter_by(is_active=True).all()
    
    sandwiches = {item.name: item.price for item in items if item.category == 'sandwich'}
    crisps = {item.name: item.price for item in items if item.category == 'crisps'}
    snacks = {item.name: item.price for item in items if item.category == 'snack'}
    premium_sandwiches = [item.name for item in items if item.category == 'sandwich' and item.is_premium]
    
    return sandwiches, crisps, snacks, premium_sandwiches


def initialize_default_menu():
    """Add default menu items if database is empty"""
    if MenuItem.query.count() == 0:
        default_items = [
            # Sandwiches
            MenuItem(name="Ham & Cheese", price=3.50, category="sandwich"),
            MenuItem(name="Tuna Mayo", price=3.50, category="sandwich"),
            MenuItem(name="Chicken Salad", price=3.50, category="sandwich"),
            MenuItem(name="BLT", price=3.50, category="sandwich"),
            MenuItem(name="Egg Mayo", price=3.50, category="sandwich"),
            MenuItem(name="Cheese & Pickle", price=3.50, category="sandwich"),
            MenuItem(name="Prawn Mayo", price=4.50, category="sandwich", is_premium=True),
            MenuItem(name="Steak & Onion", price=4.50, category="sandwich", is_premium=True),
            
            # Crisps
            MenuItem(name="Ready Salted", price=1.50, category="crisps"),
            MenuItem(name="Salt & Vinegar", price=1.50, category="crisps"),
            MenuItem(name="Cheese & Onion", price=1.50, category="crisps"),
            MenuItem(name="Prawn Cocktail", price=1.50, category="crisps"),
            MenuItem(name="BBQ", price=1.50, category="crisps"),
            MenuItem(name="Sour Cream", price=1.50, category="crisps"),
            MenuItem(name="Paprika", price=1.50, category="crisps"),
            MenuItem(name="Spicy Chili", price=1.50, category="crisps"),
            
            # Snacks
            MenuItem(name="Apple", price=1.00, category="snack"),
            MenuItem(name="Banana", price=1.00, category="snack"),
            MenuItem(name="Chocolate Bar", price=2.00, category="snack"),
            MenuItem(name="Granola Bar", price=2.00, category="snack"),
            MenuItem(name="Cookie", price=1.50, category="snack"),
            MenuItem(name="Brownie", price=2.00, category="snack"),
            MenuItem(name="Fruit Pot", price=2.50, category="snack"),
            MenuItem(name="Yogurt", price=2.00, category="snack"),
        ]
        
        db.session.add_all(default_items)
        db.session.commit()


lunch_offer_price = 5.00


def check_offer_eligibility(sandwich_choice):
    """Check if the selected items qualify for the lunch offer"""
    item = MenuItem.query.filter_by(name=sandwich_choice, category='sandwich').first()
    if item:
        return not item.is_premium
    return True


def calculate_total(sandwich, crisp, snack, qualifies_for_offer):
    """Calculate the total price"""
    if qualifies_for_offer:
        return lunch_offer_price
    else:
        sandwiches, crisps, snacks, _ = get_menu_items()
        total = sandwiches.get(sandwich, 0) + crisps.get(crisp, 0) + snacks.get(snack, 0)
        return total


# ADMIN AUTHENTICATION DECORATOR
def admin_required(f):
    """Decorator to protect admin routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function


# ROUTES
@app.route('/')
def index():
    """Home page - display the menu selection form"""
    sandwiches, crisps, snacks, premium_sandwiches = get_menu_items()
    return render_template('index.html', 
                         sandwiches=sandwiches,
                         crisps=crisps,
                         snacks=snacks,
                         premium_sandwiches=premium_sandwiches)


@app.route('/calculate', methods=['POST'])
def calculate():
    """Process the form submission, save to database, and show results"""
    sandwich_choice = request.form.get('sandwich')
    crisp_choice = request.form.get('crisp')
    snack_choice = request.form.get('snack')
    
    sandwiches, crisps, snacks, premium_sandwiches = get_menu_items()
    
    if not sandwich_choice or not crisp_choice or not snack_choice:
        return render_template('index.html',
                             sandwiches=sandwiches,
                             crisps=crisps,
                             snacks=snacks,
                             premium_sandwiches=premium_sandwiches,
                             error="Please select one item from each category")
    
    qualifies = check_offer_eligibility(sandwich_choice)
    total = calculate_total(sandwich_choice, crisp_choice, snack_choice, qualifies)
    
    savings = 0
    if qualifies:
        regular_total = sandwiches[sandwich_choice] + crisps[crisp_choice] + snacks[snack_choice]
        savings = regular_total - total
    
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
    
    db.session.add(new_order)
    db.session.commit()
    
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
    all_orders = Order.query.order_by(Order.order_date.desc()).all()
    
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


# ADMIN ROUTES
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Admin login page"""
    if request.method == 'POST':
        password = request.form.get('password')
        if password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            flash('Successfully logged in!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Incorrect password', 'error')
    
    return render_template('admin_login.html')


@app.route('/admin/logout')
def admin_logout():
    """Admin logout"""
    session.pop('admin_logged_in', None)
    flash('Logged out successfully', 'success')
    return redirect(url_for('index'))


@app.route('/admin')
@admin_required
def admin_dashboard():
    """Admin dashboard - manage menu items"""
    all_items = MenuItem.query.order_by(MenuItem.category, MenuItem.name).all()
    
    # Group by category
    sandwiches = [item for item in all_items if item.category == 'sandwich']
    crisps = [item for item in all_items if item.category == 'crisps']
    snacks = [item for item in all_items if item.category == 'snack']
    
    return render_template('admin_dashboard.html',
                         sandwiches=sandwiches,
                         crisps=crisps,
                         snacks=snacks)


@app.route('/admin/item/add', methods=['GET', 'POST'])
@admin_required
def admin_add_item():
    """Add a new menu item"""
    if request.method == 'POST':
        name = request.form.get('name')
        price = float(request.form.get('price'))
        category = request.form.get('category')
        is_premium = request.form.get('is_premium') == 'on'
        
        # Check if item already exists
        existing = MenuItem.query.filter_by(name=name).first()
        if existing:
            flash(f'Item "{name}" already exists!', 'error')
            return redirect(url_for('admin_add_item'))
        
        new_item = MenuItem(
            name=name,
            price=price,
            category=category,
            is_premium=is_premium
        )
        
        db.session.add(new_item)
        db.session.commit()
        
        flash(f'Added "{name}" successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
    
    return render_template('admin_add_item.html')


@app.route('/admin/item/edit/<int:item_id>', methods=['GET', 'POST'])
@admin_required
def admin_edit_item(item_id):
    """Edit an existing menu item"""
    item = MenuItem.query.get_or_404(item_id)
    
    if request.method == 'POST':
        item.name = request.form.get('name')
        item.price = float(request.form.get('price'))
        item.category = request.form.get('category')
        item.is_premium = request.form.get('is_premium') == 'on'
        item.is_active = request.form.get('is_active') == 'on'
        
        db.session.commit()
        
        flash(f'Updated "{item.name}" successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
    
    return render_template('admin_edit_item.html', item=item)


@app.route('/admin/item/delete/<int:item_id>', methods=['POST'])
@admin_required
def admin_delete_item(item_id):
    """Delete a menu item (soft delete - just marks as inactive)"""
    item = MenuItem.query.get_or_404(item_id)
    item.is_active = False
    db.session.commit()
    
    flash(f'Deleted "{item.name}" successfully!', 'success')
    return redirect(url_for('admin_dashboard'))


# Create database tables and initialize menu
with app.app_context():
    db.create_all()
    initialize_default_menu()


# Run the application
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=True, host='0.0.0.0', port=port)