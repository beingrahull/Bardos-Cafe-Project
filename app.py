from flask import Flask, render_template, request
from random import randint
import sqlite3
from datetime import datetime, timedelta

app = Flask(__name__)

# Connect to SQLite database
conn = sqlite3.connect('bardos_cafe.db', check_same_thread=False)
cursor = conn.cursor()




# Create tables
cursor.execute('''
    CREATE TABLE IF NOT EXISTS temp_dinein (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        mobile TEXT,
        diners INTEGER,
        preferred_time TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS temp_takeaway (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        mobile TEXT,
        address TEXT,
        payment TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS temp_delivery (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        mobile TEXT,
        address TEXT,
        payment TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')
conn.commit()

# Cleanup function
def cleanup_expired_records():
    cutoff = datetime.now() - timedelta(days=2)
    for table in ['temp_dinein', 'temp_takeaway', 'temp_delivery']:
        cursor.execute(f"DELETE FROM {table} WHERE created_at < ?", (cutoff,))
    conn.commit()

# Home route
from coffee import load_coffee_items
from bakery_pastries import load_bakery_pastries_items
from breakfast_brunch import load_breakfast_brunch_items
from savory_bites import load_savory_bites_items
from desserts import load_desserts_items
from offers_deals import load_offers_deals_items

@app.route("/")


def render():
    cleanup_expired_records()
    coffee = load_coffee_items()
    bakery_pastries = load_bakery_pastries_items()
    breakfast_brunch = load_breakfast_brunch_items()
    savory_bites = load_savory_bites_items()
    desserts = load_desserts_items()
    offers_deals=load_offers_deals_items()
    return render_template("index.html", coffee=coffee, bakery_pastries=bakery_pastries,
                           breakfast_brunch=breakfast_brunch, savory_bites=savory_bites, desserts=desserts, offers_deals=offers_deals)

@app.route("/order")
def order_landing():
    return render_template("item_landing.html")


# Dine-in route
@app.route('/submit_dinein', methods=['POST'])
def dine_in_data():
    name = request.form['Name']
    email = request.form['E-mail']
    mobile = request.form['Mobile']
    diners = request.form['Diners']
    preferred_time = request.form['PreferredTime']

    order_number = randint(100000, 999999)

    cursor.execute('''
        INSERT INTO temp_dinein (name, email, mobile, diners, preferred_time)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, email, mobile, diners, preferred_time))
    conn.commit()

    return render_template('confirmation.html', name=name, order_number=order_number)

# Take-away route
@app.route('/submit_takeaway', methods=['POST'])
def takeaway_data():
    name = request.form['Name']
    email = request.form['E-mail']
    mobile = request.form['Mobile']
    address = request.form['Address']
    payment = request.form['Payment']

    order_number = randint(100000, 999999)

    cursor.execute('''
        INSERT INTO temp_takeaway (name, email, mobile, address, payment)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, email, mobile, address, payment))
    conn.commit()

    return render_template('confirmation.html', name=name,order_number=order_number)

# Delivery route
@app.route('/submit_delivery', methods=['POST'])
def delivery_data():
    name = request.form['Name']
    email = request.form['E-mail']
    mobile = request.form['Mobile']
    address = request.form['Address']
    payment = request.form['Payment']

    order_number = randint(100000, 999999)


    cursor.execute('''
        INSERT INTO temp_delivery (name, email, mobile, address, payment)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, email, mobile, address, payment))
    conn.commit()

    return render_template('confirmation.html', name=name,order_number=order_number)


@app.route('/staff_login')
def staff_login():
    return render_template('stafflogin.html')

@app.route('/staff_auth', methods=['POST'])
def staff_auth():
    staff_id = request.form.get('staff_id')
    staff_code = request.form.get('staff_code')

    # Simple hardcoded credentials - replace with your own authentication method
    valid_credentials = {
        'staff1': 'code123',
        'staff2': 'code456'
    }

    if staff_id in valid_credentials and staff_code == valid_credentials[staff_id]:
        # Connect to DB and fetch recent orders
        conn = sqlite3.connect('bardos_cafe.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM temp_dinein ORDER BY created_at DESC LIMIT 10")
        dinein_orders = cursor.fetchall()

        cursor.execute("SELECT * FROM temp_takeaway ORDER BY created_at DESC LIMIT 10")
        takeaway_orders = cursor.fetchall()

        cursor.execute("SELECT * FROM temp_delivery ORDER BY created_at DESC LIMIT 10")
        delivery_orders = cursor.fetchall()

        conn.close()

        return render_template('staff_dashboard.html',
                               dinein_orders=dinein_orders,
                               takeaway_orders=takeaway_orders,
                               delivery_orders=delivery_orders)
    else:
        # Authentication failed, show error on login page
        return render_template('stafflogin.html', error="Invalid Staff ID or Code")





# Run the app
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
