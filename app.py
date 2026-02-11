"""
Flask Web Application for Lunch Offer Menu - PROFESSIONAL WEBSITE
Multi-page website with homepage, menu, locations, about, and admin features
"""

from flask import Flask, render_template, request, session, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from functools import wraps
from collections import defaultdict
import secrets
import os

# Create Flask application
app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# CONFIGURATION
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin123')
BUSINESS_NAME = "Fresh Bites Café"
BUSINESS_TAGLINE = "Delicious Lunch Deals, Every Day"

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
    category = db.Column(db.String(50), nullable=False)
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


# PUBLIC ROUTES
@app.route('/')
def home():
    """Homepage"""
    return render_template('home.html', business_name=BUSINESS_NAME, tagline=BUSINESS_TAGLINE)


@app.route('/menu')
def menu():
    """Menu page - display the menu selection form"""
    try:
        sandwiches, crisps, snacks, premium_sandwiches = get_menu_items()
        return render_template('menu.html', 
                             sandwiches=sandwiches,
                             crisps=crisps,
                             snacks=snacks,
                             premium_sandwiches=premium_sandwiches,
                             business_name=BUSINESS_NAME)
    except Exception as e:
        print(f"Menu error: {e}")
        # Initialize database if needed
        try:
            db.create_all()
            initialize_default_menu()
            return redirect(url_for('menu'))
        except:
            return "Database initialization required. Please contact administrator.", 500


@app.route('/locations')
def locations():
    """Locations page"""
    # You can customize these locations
    store_locations = [
        {
            'name': 'City Centre',
            'address': '123 High Street, London, EC1A 1BB',
            'phone': '020 1234 5678',
            'hours': 'Mon-Fri: 7am-6pm, Sat: 8am-4pm, Sun: Closed'
        },
        {
            'name': 'Riverside',
            'address': '45 River Walk, London, SE1 9PP',
            'phone': '020 8765 4321',
            'hours': 'Mon-Fri: 7am-6pm, Sat: 8am-4pm, Sun: Closed'
        },
        {
            'name': 'Business District',
            'address': '78 Corporate Plaza, London, EC2M 7PP',
            'phone': '020 5555 6789',
            'hours': 'Mon-Fri: 6:30am-7pm, Sat-Sun: Closed'
        }
    ]
    return render_template('locations.html', 
                         locations=store_locations,
                         business_name=BUSINESS_NAME)


@app.route('/about')
def about():
    """About page"""
    return render_template('about.html', business_name=BUSINESS_NAME)


@app.route('/calculate', methods=['POST'])
def calculate():
    """Process the form submission, save to database, and show results"""
    sandwich_choice = request.form.get('sandwich')
    crisp_choice = request.form.get('crisp')
    snack_choice = request.form.get('snack')
    
    sandwiches, crisps, snacks, premium_sandwiches = get_menu_items()
    
    if not sandwich_choice or not crisp_choice or not snack_choice:
        return render_template('menu.html',
                             sandwiches=sandwiches,
                             crisps=crisps,
                             snacks=snacks,
                             premium_sandwiches=premium_sandwiches,
                             business_name=BUSINESS_NAME,
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
                         order_id=new_order.id,
                         business_name=BUSINESS_NAME)


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
                         offers_applied=offers_applied,
                         business_name=BUSINESS_NAME)


# ANALYTICS ROUTES
@app.route('/analytics')
@admin_required
def analytics():
    """Sales analytics dashboard with charts"""
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=30)
    
    all_orders = Order.query.all()
    recent_orders = Order.query.filter(Order.order_date >= start_date).all()
    
    total_orders = len(all_orders)
    total_revenue = sum(order.total_price for order in all_orders)
    total_savings = sum(order.savings for order in all_orders)
    avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
    
    return render_template('analytics.html',
                         total_orders=total_orders,
                         total_revenue=total_revenue,
                         total_savings=total_savings,
                         avg_order_value=avg_order_value,
                         business_name=BUSINESS_NAME)


@app.route('/api/analytics/daily-sales')
@admin_required
def api_daily_sales():
    """API endpoint for daily sales data"""
    days = int(request.args.get('days', 30))
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    orders = Order.query.filter(Order.order_date >= start_date).all()
    
    daily_sales = defaultdict(float)
    daily_orders = defaultdict(int)
    
    for order in orders:
        date_key = order.order_date.strftime('%Y-%m-%d')
        daily_sales[date_key] += order.total_price
        daily_orders[date_key] += 1
    
    dates = sorted(daily_sales.keys())
    sales = [daily_sales[date] for date in dates]
    order_counts = [daily_orders[date] for date in dates]
    
    return jsonify({
        'dates': dates,
        'sales': sales,
        'orders': order_counts
    })


@app.route('/api/analytics/top-items')
@admin_required
def api_top_items():
    """API endpoint for top selling items by category"""
    all_orders = Order.query.all()
    
    sandwich_counts = defaultdict(int)
    crisps_counts = defaultdict(int)
    snack_counts = defaultdict(int)
    
    for order in all_orders:
        sandwich_counts[order.sandwich] += 1
        crisps_counts[order.crisps] += 1
        snack_counts[order.snack] += 1
    
    top_sandwiches = sorted(sandwich_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    top_crisps = sorted(crisps_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    top_snacks = sorted(snack_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    
    return jsonify({
        'sandwiches': {
            'labels': [item[0] for item in top_sandwiches],
            'data': [item[1] for item in top_sandwiches]
        },
        'crisps': {
            'labels': [item[0] for item in top_crisps],
            'data': [item[1] for item in top_crisps]
        },
        'snacks': {
            'labels': [item[0] for item in top_snacks],
            'data': [item[1] for item in top_snacks]
        }
    })


@app.route('/api/analytics/offer-stats')
@admin_required
def api_offer_stats():
    """API endpoint for offer vs regular pricing stats"""
    all_orders = Order.query.all()
    
    offer_count = sum(1 for order in all_orders if order.offer_applied)
    regular_count = len(all_orders) - offer_count
    
    return jsonify({
        'labels': ['Lunch Offer Applied', 'Regular Pricing'],
        'data': [offer_count, regular_count]
    })


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
    
    return render_template('admin_login.html', business_name=BUSINESS_NAME)


@app.route('/admin/logout')
def admin_logout():
    """Admin logout"""
    session.pop('admin_logged_in', None)
    flash('Logged out successfully', 'success')
    return redirect(url_for('home'))


@app.route('/admin')
@admin_required
def admin_dashboard():
    """Admin dashboard - manage menu items"""
    try:
        all_items = MenuItem.query.order_by(MenuItem.category, MenuItem.name).all()
        
        sandwiches = [item for item in all_items if item.category == 'sandwich']
        crisps = [item for item in all_items if item.category == 'crisps']
        snacks = [item for item in all_items if item.category == 'snack']
        
        return render_template('admin_dashboard.html',
                             sandwiches=sandwiches,
                             crisps=crisps,
                             snacks=snacks,
                             business_name=BUSINESS_NAME)
    except Exception as e:
        # If database tables don't exist, create them
        print(f"Admin dashboard error: {e}")
        try:
            db.create_all()
            initialize_default_menu()
            flash('Database initialized. Please try again.', 'success')
            return redirect(url_for('admin_dashboard'))
        except Exception as e2:
            flash(f'Database error: {str(e2)}. Please contact support.', 'error')
            return redirect(url_for('home'))


@app.route('/admin/item/add', methods=['GET', 'POST'])
@admin_required
def admin_add_item():
    """Add a new menu item"""
    if request.method == 'POST':
        name = request.form.get('name')
        price = float(request.form.get('price'))
        category = request.form.get('category')
        is_premium = request.form.get('is_premium') == 'on'
        
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
    
    return render_template('admin_add_item.html', business_name=BUSINESS_NAME)


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
    
    return render_template('admin_edit_item.html', item=item, business_name=BUSINESS_NAME)


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
    try:
        db.create_all()
        print("Database tables created successfully")
        initialize_default_menu()
        print("Default menu initialized")
    except Exception as e:
        print(f"Database initialization error: {e}")
        # Continue anyway - tables might already exist


# Run the application
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=True, host='0.0.0.0', port=port)