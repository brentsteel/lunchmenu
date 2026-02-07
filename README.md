# Lunch Offer Menu - Flask Web Application

A simple Flask web application for learning Python and web development concepts.

## What You'll Learn

- **Python**: Variables, dictionaries, lists, functions, conditional logic
- **Flask**: Routes, templates, forms, request handling
- **HTML**: Structure, forms, semantic markup
- **CSS**: Styling, layouts, responsive design

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

### 1. Install Flask

First, you need to install Flask. Open your terminal and run:

```bash
pip install flask
```

### 2. Run the Application

Navigate to the folder containing `app.py` and run:

```bash
python app.py
```

You should see output like:
```
 * Running on http://0.0.0.0:5000
 * Running on http://127.0.0.1:5000
```

### 3. Open in Browser

Open your web browser and go to:
```
http://127.0.0.1:5000
```

or

```
http://localhost:5000
```

## How It Works

### Flask App (app.py)

1. **Menu Data**: Stores sandwiches, crisps, and snacks in dictionaries
2. **Routes**: 
   - `/` - Shows the menu selection page
   - `/calculate` - Processes the form and shows results
3. **Logic**: Checks if sandwich is premium and calculates total

### Templates

- **index.html**: Form with radio buttons for menu selections
- **result.html**: Displays order summary and total price

### The Flow

1. User visits homepage (`/`)
2. Selects sandwich, crisps, and snack
3. Clicks "Calculate My Order"
4. Form submits to `/calculate` route
5. Python checks eligibility and calculates total
6. Results page displays order summary

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
