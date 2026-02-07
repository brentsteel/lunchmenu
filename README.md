# Lunch Offer Menu - Flask Web Application with Database

A Flask web application that saves orders to a database and displays order history.

## What You'll Learn

- **Python**: Variables, dictionaries, lists, functions, conditional logic
- **Flask**: Routes, templates, forms, request handling
- **Database**: SQLAlchemy ORM, PostgreSQL, data persistence
- **HTML**: Structure, forms, semantic markup
- **CSS**: Styling, layouts, responsive design

## Features

- ✅ Interactive menu selection
- ✅ Lunch offer calculation (£5 for sandwich + crisps + snack)
- ✅ Premium items exclusion
- ✅ **Database storage** - all orders are saved
- ✅ **Order history** - view all past orders with statistics
- ✅ Local development (SQLite) and production (PostgreSQL) support

## Project Structure

```
lunch-menu/
│
├── app.py                 # Main Flask application (Python logic)
├── lunch_menu.py         # Original command-line version
│
└── templates/            # HTML templates folder
    ├── index.html        # Menu selection page
    └── result.html       # Order summary page
```

## Setup Instructions

### 1. Install Dependencies

Install Flask and database packages:

```bash
pip install -r requirements.txt
```

This installs:
- Flask (web framework)
- Flask-SQLAlchemy (database toolkit)
- psycopg2-binary (PostgreSQL driver)
- gunicorn (production server)

### 2. Local Development (SQLite)

For local testing, the app automatically uses SQLite (no setup needed):

```bash
python app.py
```

A file called `orders.db` will be created automatically to store your orders locally.

### 3. Open in Browser

Open your web browser and go to:
```
http://127.0.0.1:5000
```

or

```
http://localhost:5000
```

## Database Setup for Production (Render)

### 1. Create PostgreSQL Database on Render

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **New +** → **PostgreSQL**
3. Configure:
   - Name: `lunch-menu-db`
   - Database: `lunch_orders` (or any name)
   - User: (auto-generated)
   - Region: Choose closest to you
   - Instance Type: **Free**
4. Click **Create Database**
5. Wait for it to be created (takes ~1 minute)

### 2. Connect Database to Web Service

1. Go to your web service on Render
2. Click **Environment** in the left menu
3. Click **Add Environment Variable**
4. Add:
   - Key: `DATABASE_URL`
   - Value: Copy the **Internal Database URL** from your PostgreSQL database page
5. Click **Save Changes**

Your app will automatically restart and connect to PostgreSQL!

### 3. How it Works

- **Local development**: Uses SQLite (`orders.db` file)
- **Production (Render)**: Uses PostgreSQL (cloud database)
- The app automatically detects which to use based on the `DATABASE_URL` environment variable

## How It Works

### Flask App (app.py)

1. **Menu Data**: Stores sandwiches, crisps, and snacks in dictionaries
2. **Routes**: 
   - `/` - Shows the menu selection page
   - `/calculate` - Processes the form and shows results
   - `/history` - Displays all past orders from database
3. **Database**: Saves every order with all details and timestamps

### Templates

- **index.html**: Form with radio buttons for menu selections
- **result.html**: Displays order summary and total price
- **history.html**: Shows all orders with statistics (total revenue, savings, etc.)

### The Flow

1. User visits homepage (`/`)
2. Selects sandwich, crisps, and snack
3. Clicks "Calculate My Order"
4. Form submits to `/calculate` route
5. Python checks eligibility and calculates total
6. **Order is saved to database**
7. Results page displays order summary with order ID
8. User can view `/history` to see all past orders

## Experimenting & Learning

Try modifying these to learn:

### In app.py:
- Add new menu items to dictionaries
- Change the offer price
- Add more premium items
- Create a new category (drinks?)

### In index.html:
- Change colors in the CSS section
- Modify the layout grid
- Add images for menu items

### In result.html:
- Change the success/warning styling
- Add more details to the summary
- Create a "print receipt" button

## Key Concepts Explained

### Flask Routes
```python
@app.route('/')
def index():
    # This runs when someone visits the homepage
```

### Jinja2 Templates
```html
{% for name, price in sandwiches.items() %}
    <!-- This loops through all sandwiches -->
{% endfor %}
```

### Form Handling
```python
request.form.get('sandwich')  # Gets the selected sandwich from the form
```

## Troubleshooting

**Port already in use?**
- Change the port in app.py: `app.run(port=5001)`

**Template not found?**
- Make sure the `templates` folder is in the same directory as `app.py`

**Changes not showing?**
- Hard refresh your browser (Ctrl+F5 or Cmd+Shift+R)
- Make sure debug=True is set in app.py

## Next Steps

Once comfortable, you could:
- Add a database to store orders
- Create user accounts
- Add a shopping cart for multiple orders
- Deploy to the internet (Heroku, PythonAnywhere)
- Add JavaScript for dynamic interactions

## Resources

- Flask Documentation: https://flask.palletsprojects.com/
- HTML/CSS Tutorial: https://www.w3schools.com/
- Python Tutorial: https://docs.python.org/3/tutorial/

Happy coding! 🚀