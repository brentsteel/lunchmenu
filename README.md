# Fresh Bites Café - Professional Multi-Page Website

A complete Flask web application with professional design, multi-page structure, admin panel, and sales analytics.

## What You'll Learn

- **Python**: Variables, dictionaries, lists, functions, conditional logic
- **Flask**: Routes, templates, forms, request handling
- **Database**: SQLAlchemy ORM, PostgreSQL, data persistence
- **HTML**: Structure, forms, semantic markup
- **CSS**: Styling, layouts, responsive design

## Features

### Public-Facing Website
- ✅ **Professional Homepage** - Hero section, features grid, call-to-action
- ✅ **Menu Page** - Interactive menu selection with lunch deal
- ✅ **Locations Page** - Multiple store locations with contact details
- ✅ **About Page** - Company story, values, and mission
- ✅ **Responsive Design** - Works on desktop, tablet, and mobile
- ✅ **Professional Branding** - Consistent design with custom logo and colors

### Business Features
- ✅ **Order Management** - Save all orders to database
- ✅ **Order History** - View all past orders with statistics
- ✅ **Lunch Offer Calculation** - £5 for sandwich + crisps + snack
- ✅ **Premium Items** - Exclude certain items from offer

### Admin Features  
- ✅ **Admin Panel** - Password-protected dashboard
- ✅ **Menu Management** - Add, edit, delete menu items
- ✅ **Sales Analytics** - Interactive charts and graphs
- ✅ **Real-time Data** - All stats update automatically

### Technical
- ✅ Local development (SQLite) and production (PostgreSQL) support
- ✅ RESTful API endpoints for analytics
- ✅ Session-based authentication

## Project Structure

```
fresh-bites-cafe/
│
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── README.md                   # This file
│
├── static/                     # Static files
│   ├── css/
│   │   └── style.css          # Main stylesheet
│   └── images/                # Logo and images (add your own)
│
└── templates/                  # HTML templates
    ├── home.html              # Homepage
    ├── menu.html              # Menu selection page
    ├── locations.html         # Store locations
    ├── about.html             # About us page
    ├── result.html            # Order confirmation
    ├── history.html           # Order history
    ├── analytics.html         # Sales analytics (admin)
    ├── admin_login.html       # Admin login
    ├── admin_dashboard.html   # Admin menu management
    ├── admin_add_item.html    # Add menu item form
    └── admin_edit_item.html   # Edit menu item form
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

### 4. Set Admin Password (Important!)

For security, set an admin password as an environment variable on Render:

1. Go to your web service settings
2. Click **Environment** tab
3. Add environment variable:
   - Key: `ADMIN_PASSWORD`
   - Value: Your secure password (e.g., `MySecurePass123!`)
4. Click **Save Changes**

**Local Development**: The default password is `admin123` (change this in production!)

### 5. How it Works

- **Local development**: Uses SQLite (`orders.db` file)
- **Production (Render)**: Uses PostgreSQL (cloud database)
- The app automatically detects which to use based on the `DATABASE_URL` environment variable

## How It Works

### Flask App (app.py)

1. **Business Configuration**: Company name, tagline, pricing stored at top
2. **Public Routes**: 
   - `/` - Homepage with hero section and features
   - `/menu` - Menu selection page
   - `/locations` - Store locations
   - `/about` - About us page
   - `/calculate` - Processes orders
   - `/history` - Order history
3. **Admin Routes**: 
   - `/admin` - Admin dashboard (password protected)
   - `/admin/login` - Admin login page
   - `/admin/item/add` - Add menu items
   - `/admin/item/edit/<id>` - Edit items
   - `/analytics` - Sales analytics dashboard
4. **API Endpoints**:
   - `/api/analytics/daily-sales` - Daily sales data
   - `/api/analytics/top-items` - Best selling items
   - `/api/analytics/offer-stats` - Offer usage stats

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

## Using the Admin Panel

### Accessing Admin

1. Visit `/admin` or click the "🔐 Admin" link on the menu page
2. Enter the admin password (default: `admin123` locally)
3. You'll be taken to the admin dashboard

### Managing Menu Items

**Add New Items:**
1. Click "+ Add Item" button
2. Fill in item name, price, category
3. Check "Premium Item" if it shouldn't qualify for the £5 offer
4. Click "Add Item"

**Edit Items:**
1. Click "Edit" button next to any item
2. Update name, price, category, or premium status
3. Uncheck "Active" to hide an item from the menu without deleting it
4. Click "Save Changes"

**Delete Items:**
1. Click "Delete" button next to any item
2. Confirm deletion
3. Item will be marked as inactive (soft delete - not permanently removed)

**Security Note:** Always change the default admin password in production!

## Sales Analytics Dashboard

The analytics dashboard provides visual insights into your sales data:

**Access:** Visit `/analytics` (requires admin login)

**Features:**
- **Overview Stats**: Total orders, revenue, customer savings, and average order value
- **Daily Sales Chart**: Line graph showing revenue and order trends over last 30 days
- **Top Items**: Bar charts and pie charts showing most popular items by category
- **Offer Statistics**: Pie chart showing how many orders used the lunch offer vs regular pricing

**Charts Available:**
1. Daily Sales (Line Chart) - Revenue and order count trends
2. Top Sandwiches (Horizontal Bar Chart) - Best selling sandwiches
3. Top Crisps (Doughnut Chart) - Most popular crisps flavors
4. Top Snacks (Doughnut Chart) - Most ordered snacks
5. Offer Application (Pie Chart) - Lunch offer vs regular pricing breakdown

All charts are interactive and built with Chart.js!

## Customizing Your Website

### Change Business Name and Branding

In `app.py`, update these lines (around line 22-23):
```python
BUSINESS_NAME = "Fresh Bites Café"
BUSINESS_TAGLINE = "Delicious Lunch Deals, Every Day"
```

### Change Colors and Styling

Edit `/static/css/style.css` and modify the CSS variables:
```css
:root {
    --primary-color: #2ecc71;    /* Main brand color */
    --secondary-color: #27ae60;  /* Secondary brand color */
    --accent-color: #f39c12;     /* Accent color */
    --dark-color: #2c3e50;       /* Dark text */
}
```

### Add Your Logo

1. Add your logo image to `/static/images/logo.png`
2. In templates, replace the emoji logo:
```html
<!-- Change from: -->
<span class="logo-icon">🥪</span>

<!-- To: -->
<img src="{{ url_for('static', filename='images/logo.png') }}" alt="Logo" style="height: 40px;">
```

### Update Store Locations

In `app.py`, find the `/locations` route (around line 180) and modify the `store_locations` array:
```python
store_locations = [
    {
        'name': 'Your Location Name',
        'address': 'Your Address',
        'phone': 'Your Phone',
        'hours': 'Your Hours'
    },
    # Add more locations...
]
```

### Customize Menu Items

Log in to the admin panel (`/admin`) and use the interface to:
- Add new menu items
- Edit prices
- Mark items as premium
- Activate/deactivate items

### Update Footer Information

Edit the footer section in each template file to change:
- Contact information
- Opening hours
- Social media links
- Company description

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