import sqlite3
from datetime import date, timedelta

DATABASE = "localsync.db"


def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def init_database():
    connection = get_connection()
    cursor = connection.cursor()

    # -------------------------
    # CUSTOMERS
    # -------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL UNIQUE,
            language TEXT DEFAULT 'Hindi',
            address TEXT DEFAULT '',
            status TEXT DEFAULT 'Active',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # -------------------------
    # PRODUCTS
    # -------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT DEFAULT 'Grocery',
            price REAL NOT NULL,
            stock INTEGER DEFAULT 0,
            unit TEXT DEFAULT 'pcs',
            status TEXT DEFAULT 'Available',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # -------------------------
    # CUSTOMER PURCHASE CYCLES
    # -------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customer_products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            customer_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,

            cycle_days INTEGER DEFAULT 25,

            last_purchase_date TEXT,
            next_reminder_date TEXT,

            total_purchases INTEGER DEFAULT 0,

            snooze_count INTEGER DEFAULT 0,

            created_at TEXT DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(customer_id)
                REFERENCES customers(id)
                ON DELETE CASCADE,

            FOREIGN KEY(product_id)
                REFERENCES products(id)
                ON DELETE CASCADE,

            UNIQUE(customer_id, product_id)
        )
    """)

    # -------------------------
    # ORDERS
    # -------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            customer_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,

            quantity INTEGER DEFAULT 1,

            fulfilment TEXT DEFAULT 'Pickup',

            status TEXT DEFAULT 'Pending',

            total_amount REAL DEFAULT 0,

            created_at TEXT DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(customer_id)
                REFERENCES customers(id)
                ON DELETE CASCADE,

            FOREIGN KEY(product_id)
                REFERENCES products(id)
                ON DELETE CASCADE
        )
    """)

    # -------------------------
    # REMINDER LOG
    # -------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reminder_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            customer_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,

            response TEXT,

            old_cycle INTEGER,
            new_cycle INTEGER,

            created_at TEXT DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(customer_id)
                REFERENCES customers(id)
                ON DELETE CASCADE,

            FOREIGN KEY(product_id)
                REFERENCES products(id)
                ON DELETE CASCADE
        )
    """)

    connection.commit()
    connection.close()


# ==========================================================
# DEMO DATA
# ==========================================================

def seed_demo_data():

    connection = get_connection()
    cursor = connection.cursor()

    existing = cursor.execute(
        "SELECT COUNT(*) AS count FROM customers"
    ).fetchone()["count"]

    if existing > 0:
        connection.close()
        return

    customers = [
        (
            "Amit Sharma",
            "9876543210",
            "Hindi",
            "Green Park Society"
        ),
        (
            "Ramesh Kumar",
            "9123456780",
            "Telugu",
            "Sai Residency"
        ),
        (
            "Priya Menon",
            "9988776655",
            "English",
            "Lake View Apartments"
        ),
        (
            "Arjun Rao",
            "9001122334",
            "Kannada",
            "Sunrise Colony"
        ),
        (
            "Sneha Patel",
            "9887766554",
            "Hindi",
            "Shanti Nagar"
        )
    ]

    for customer in customers:

        cursor.execute("""
            INSERT INTO customers
            (name, phone, language, address)
            VALUES (?, ?, ?, ?)
        """, customer)

    products = [
        ("Aashirvaad Atta 10kg", "Staples", 450, 34, "bag"),
        ("Tata Salt 1kg", "Staples", 28, 72, "pack"),
        ("Fortune Sunflower Oil 1L", "Cooking Oil", 145, 41, "bottle"),
        ("Amul Milk 1L", "Dairy", 68, 28, "packet"),
        ("Tata Tea 500g", "Beverages", 265, 19, "pack"),
        ("India Gate Basmati Rice 5kg", "Staples", 620, 16, "bag")
    ]

    for product in products:

        cursor.execute("""
            INSERT INTO products
            (name, category, price, stock, unit)
            VALUES (?, ?, ?, ?, ?)
        """, product)

    connection.commit()

    customer_rows = cursor.execute(
        "SELECT id, name FROM customers"
    ).fetchall()

    product_rows = cursor.execute(
        "SELECT id, name FROM products"
    ).fetchall()

    today = date.today()

    # Create realistic demo consumption records
    for customer in customer_rows:

        # Each customer gets 1-2 tracked products
        selected_products = product_rows[:2]

        for index, product in enumerate(selected_products):

            if customer["id"] % 2 == 0:
                cycle = 30
            else:
                cycle = 25

            last_purchase = today - timedelta(days=cycle)

            # First customer is due today
            if customer["id"] == 1 and index == 0:
                next_reminder = today
            else:
                next_reminder = today + timedelta(days=index + 2)

            cursor.execute("""
                INSERT INTO customer_products
                (
                    customer_id,
                    product_id,
                    cycle_days,
                    last_purchase_date,
                    next_reminder_date,
                    total_purchases
                )
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                customer["id"],
                product["id"],
                cycle,
                last_purchase.isoformat(),
                next_reminder.isoformat(),
                4
            ))

    connection.commit()
    connection.close()


# ==========================================================
# DASHBOARD
# ==========================================================

def get_dashboard_data():

    connection = get_connection()
    cursor = connection.cursor()

    customers = cursor.execute("""
        SELECT COUNT(*) AS count
        FROM customers
        WHERE status = 'Active'
    """).fetchone()["count"]

    products = cursor.execute("""
        SELECT COUNT(*) AS count
        FROM products
        WHERE status = 'Available'
    """).fetchone()["count"]

    pending_orders = cursor.execute("""
        SELECT COUNT(*) AS count
        FROM orders
        WHERE status = 'Pending'
    """).fetchone()["count"]

    reminders_due = cursor.execute("""
        SELECT COUNT(*) AS count
        FROM customer_products
        WHERE date(next_reminder_date) <= date('now')
    """).fetchone()["count"]

    revenue = cursor.execute("""
        SELECT COALESCE(SUM(total_amount), 0) AS total
        FROM orders
        WHERE date(created_at) = date('now')
    """).fetchone()["total"]

    recent_orders = cursor.execute("""
        SELECT
            orders.id,
            customers.name AS customer_name,
            products.name AS product_name,
            orders.quantity,
            orders.fulfilment,
            orders.status,
            orders.total_amount,
            orders.created_at
        FROM orders
        JOIN customers
            ON orders.customer_id = customers.id
        JOIN products
            ON orders.product_id = products.id
        ORDER BY orders.id DESC
        LIMIT 5
    """).fetchall()

    due_reminders = cursor.execute("""
        SELECT
            customer_products.id,
            customers.name AS customer_name,
            products.name AS product_name,
            customer_products.cycle_days,
            customer_products.next_reminder_date
        FROM customer_products
        JOIN customers
            ON customer_products.customer_id = customers.id
        JOIN products
            ON customer_products.product_id = products.id
        WHERE date(customer_products.next_reminder_date) <= date('now')
        ORDER BY customer_products.next_reminder_date
        LIMIT 5
    """).fetchall()

    connection.close()

    return {
        "customers": customers,
        "products": products,
        "orders": pending_orders,
        "reminders": reminders_due,
        "revenue": revenue,
        "recent_orders": [dict(row) for row in recent_orders],
        "due_reminders": [dict(row) for row in due_reminders]
    }


# ==========================================================
# CUSTOMERS
# ==========================================================

def get_customers(search=""):

    connection = get_connection()
    cursor = connection.cursor()

    if search:

        rows = cursor.execute("""
            SELECT *
            FROM customers
            WHERE name LIKE ?
               OR phone LIKE ?
            ORDER BY id DESC
        """, (
            f"%{search}%",
            f"%{search}%"
        )).fetchall()

    else:

        rows = cursor.execute("""
            SELECT *
            FROM customers
            ORDER BY id DESC
        """).fetchall()

    connection.close()

    return [dict(row) for row in rows]


def add_customer(name, phone, language, address):

    connection = get_connection()

    try:

        connection.execute("""
            INSERT INTO customers
            (name, phone, language, address)
            VALUES (?, ?, ?, ?)
        """, (
            name,
            phone,
            language,
            address
        ))

        connection.commit()

        return True, "Customer added successfully."

    except sqlite3.IntegrityError:

        return False, "A customer with this phone number already exists."

    finally:

        connection.close()


# ==========================================================
# PRODUCTS
# ==========================================================

def get_products(search=""):

    connection = get_connection()
    cursor = connection.cursor()

    if search:

        rows = cursor.execute("""
            SELECT *
            FROM products
            WHERE name LIKE ?
               OR category LIKE ?
            ORDER BY id DESC
        """, (
            f"%{search}%",
            f"%{search}%"
        )).fetchall()

    else:

        rows = cursor.execute("""
            SELECT *
            FROM products
            ORDER BY id DESC
        """).fetchall()

    connection.close()

    return [dict(row) for row in rows]


def add_product(name, category, price, stock, unit):

    connection = get_connection()

    connection.execute("""
        INSERT INTO products
        (name, category, price, stock, unit)
        VALUES (?, ?, ?, ?, ?)
    """, (
        name,
        category,
        price,
        stock,
        unit
    ))

    connection.commit()
    connection.close()


# ==========================================================
# ORDERS
# ==========================================================

def get_orders():

    connection = get_connection()

    rows = connection.execute("""
        SELECT
            orders.id,
            customers.name AS customer_name,
            products.name AS product_name,
            orders.quantity,
            orders.fulfilment,
            orders.status,
            orders.total_amount,
            orders.created_at
        FROM orders
        JOIN customers
            ON orders.customer_id = customers.id
        JOIN products
            ON orders.product_id = products.id
        ORDER BY orders.id DESC
    """).fetchall()

    connection.close()

    return [dict(row) for row in rows]


# ==========================================================
# REMINDERS
# ==========================================================

def get_reminders():

    connection = get_connection()

    rows = connection.execute("""
        SELECT
            customer_products.id,
            customers.name AS customer_name,
            customers.phone,
            customers.language,
            products.name AS product_name,
            products.price,
            customer_products.cycle_days,
            customer_products.last_purchase_date,
            customer_products.next_reminder_date,
            customer_products.total_purchases,
            customer_products.snooze_count
        FROM customer_products

        JOIN customers
            ON customer_products.customer_id = customers.id

        JOIN products
            ON customer_products.product_id = products.id

        ORDER BY customer_products.next_reminder_date
    """).fetchall()

    connection.close()

    return [dict(row) for row in rows]


# ==========================================================
# ADAPTIVE RESTOCK ENGINE
# ==========================================================

def process_reminder_response(
    customer_product_id,
    response
):

    connection = get_connection()
    cursor = connection.cursor()

    record = cursor.execute("""
        SELECT *
        FROM customer_products
        WHERE id = ?
    """, (
        customer_product_id,
    )).fetchone()

    if not record:
        connection.close()
        return False, "Customer product record not found."

    old_cycle = record["cycle_days"]

    response = str(response)

    # ------------------------------------------------------
    # RESPONSE 1 — CUSTOMER WANTS TO ORDER
    # ------------------------------------------------------

    if response == "1":

        customer_id = record["customer_id"]
        product_id = record["product_id"]

        product = cursor.execute("""
            SELECT price
            FROM products
            WHERE id = ?
        """, (
            product_id,
        )).fetchone()

        price = product["price"]

        cursor.execute("""
            INSERT INTO orders
            (
                customer_id,
                product_id,
                quantity,
                fulfilment,
                status,
                total_amount
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            customer_id,
            product_id,
            1,
            "Delivery",
            "Pending",
            price
        ))

        # Reset reminder using the current cycle
        next_date = date.today() + timedelta(days=old_cycle)

        cursor.execute("""
            UPDATE customer_products
            SET
                last_purchase_date = ?,
                next_reminder_date = ?,
                total_purchases = total_purchases + 1
            WHERE id = ?
        """, (
            date.today().isoformat(),
            next_date.isoformat(),
            customer_product_id
        ))

        cursor.execute("""
            INSERT INTO reminder_logs
            (
                customer_id,
                product_id,
                response,
                old_cycle,
                new_cycle
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            customer_id,
            product_id,
            "ORDER",
            old_cycle,
            old_cycle
        ))

        connection.commit()
        connection.close()

        return True, "Order created successfully."

    # ------------------------------------------------------
    # RESPONSE 2 — SELF PICKUP
    # ------------------------------------------------------

    elif response == "2":

        customer_id = record["customer_id"]
        product_id = record["product_id"]

        product = cursor.execute("""
            SELECT price
            FROM products
            WHERE id = ?
        """, (
            product_id,
        )).fetchone()

        price = max(0, product["price"] - 10)

        cursor.execute("""
            INSERT INTO orders
            (
                customer_id,
                product_id,
                quantity,
                fulfilment,
                status,
                total_amount
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            customer_id,
            product_id,
            1,
            "Self Pickup",
            "Pending",
            price
        ))

        next_date = date.today() + timedelta(days=old_cycle)

        cursor.execute("""
            UPDATE customer_products
            SET
                last_purchase_date = ?,
                next_reminder_date = ?,
                total_purchases = total_purchases + 1
            WHERE id = ?
        """, (
            date.today().isoformat(),
            next_date.isoformat(),
            customer_product_id
        ))

        cursor.execute("""
            INSERT INTO reminder_logs
            (
                customer_id,
                product_id,
                response,
                old_cycle,
                new_cycle
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            customer_id,
            product_id,
            "PICKUP",
            old_cycle,
            old_cycle
        ))

        connection.commit()
        connection.close()

        return True, "Pickup order created successfully."

    # ------------------------------------------------------
    # RESPONSE 3 — CUSTOMER STILL HAS STOCK
    # ------------------------------------------------------

    elif response == "3":

        # Simple adaptive rule:
        # Customer needs more time, so extend cycle by 5 days.
        new_cycle = old_cycle + 5

        next_date = date.today() + timedelta(days=5)

        cursor.execute("""
            UPDATE customer_products

            SET
                cycle_days = ?,
                next_reminder_date = ?,
                snooze_count = snooze_count + 1

            WHERE id = ?
        """, (
            new_cycle,
            next_date.isoformat(),
            customer_product_id
        ))

        cursor.execute("""
            INSERT INTO reminder_logs
            (
                customer_id,
                product_id,
                response,
                old_cycle,
                new_cycle
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            record["customer_id"],
            record["product_id"],
            "SNOOZE",
            old_cycle,
            new_cycle
        ))

        connection.commit()
        connection.close()

        return True, (
            f"Consumption cycle updated from "
            f"{old_cycle} to {new_cycle} days."
        )

    else:

        connection.close()

        return False, "Invalid response. Use 1, 2 or 3."