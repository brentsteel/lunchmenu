"""
Flask Web Application for Lunch Offer Menu
This connects our Python logic to a web interface
"""

from flask import Flask, render_template, request, session
import secrets

# Create a Flask application instance
app = Flask(__name__)
# Secret key needed for sessions (to remember user's selections)
app.secret_key = secrets.token_hex(16)

# Same menu data from our original script
sandwiches = {
    "Ham & Cheese": 3.50,
    "Tuna Mayo": 3.50,
    "Chicken Salad": 3.50,
    "BLT": 3.50,
    "Egg Mayo": 3.50,
    "Cheese & Pickle": 3.50,
    "Prawn Mayo": 4.50,  # Premium
    "Steak & Onion": 4.50  # Premium
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


# ROUTES: These are the different pages/URLs in our web app
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
    """Process the form submission and show results"""
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
    
    # Calculate savings if offer applied
    savings = 0
    if qualifies:
        regular_total = sandwiches[sandwich_choice] + crisps[crisp_choice] + snacks[snack_choice]
        savings = regular_total - total
    
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
                         snack_price=snacks[snack_choice])


# Run the application
if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=True, host='0.0.0.0', port=port)
