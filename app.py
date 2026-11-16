from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect,
    url_for
)

from database import (
    init_database,
    seed_demo_data,
    get_dashboard_data,
    get_customers,
    add_customer,
    get_products,
    add_product,
    get_orders,
    get_reminders,
    process_reminder_response
)


app = Flask(__name__)


# ==========================================================
# APPLICATION STARTUP
# ==========================================================

init_database()
seed_demo_data()


# ==========================================================
# PAGES
# ==========================================================

@app.route("/")
def dashboard():

    return render_template(
        "dashboard.html"
    )


@app.route("/customers")
def customers():

    return render_template(
        "customers.html"
    )


@app.route("/products")
def products():

    return render_template(
        "products.html"
    )


@app.route("/orders")
def orders():

    return render_template(
        "orders.html"
    )


@app.route("/reminders")
def reminders():

    return render_template(
        "reminders.html"
    )


# ==========================================================
# DASHBOARD API
# ==========================================================

@app.route("/api/dashboard")
def dashboard_api():

    return jsonify(
        get_dashboard_data()
    )


# ==========================================================
# CUSTOMER API
# ==========================================================

@app.route("/api/customers")
def customers_api():

    search = request.args.get(
        "search",
        ""
    )

    return jsonify(
        get_customers(search)
    )


@app.route("/api/customers", methods=["POST"])
def create_customer():

    data = request.get_json()

    name = data.get("name", "").strip()
    phone = data.get("phone", "").strip()
    language = data.get("language", "Hindi")
    address = data.get("address", "").strip()

    if not name or not phone:

        return jsonify({
            "success": False,
            "message": "Name and phone number are required."
        }), 400

    success, message = add_customer(
        name,
        phone,
        language,
        address
    )

    return jsonify({
        "success": success,
        "message": message
    })


# ==========================================================
# PRODUCT API
# ==========================================================

@app.route("/api/products")
def products_api():

    search = request.args.get(
        "search",
        ""
    )

    return jsonify(
        get_products(search)
    )


@app.route("/api/products", methods=["POST"])
def create_product():

    data = request.get_json()

    name = data.get("name", "").strip()
    category = data.get(
        "category",
        "Grocery"
    )

    price = float(
        data.get("price", 0)
    )

    stock = int(
        data.get("stock", 0)
    )

    unit = data.get(
        "unit",
        "pcs"
    )

    if not name or price <= 0:

        return jsonify({
            "success": False,
            "message": "Enter a valid product and price."
        }), 400

    add_product(
        name,
        category,
        price,
        stock,
        unit
    )

    return jsonify({
        "success": True,
        "message": "Product added successfully."
    })


# ==========================================================
# ORDERS API
# ==========================================================

@app.route("/api/orders")
def orders_api():

    return jsonify(
        get_orders()
    )


# ==========================================================
# REMINDERS API
# ==========================================================

@app.route("/api/reminders")
def reminders_api():

    return jsonify(
        get_reminders()
    )


# ==========================================================
# REMINDER RESPONSE
# ==========================================================

@app.route(
    "/api/reminders/<int:reminder_id>/respond",
    methods=["POST"]
)
def reminder_response(reminder_id):

    data = request.get_json()

    response = data.get(
        "response",
        ""
    )

    success, message = process_reminder_response(
        reminder_id,
        response
    )

    return jsonify({
        "success": success,
        "message": message
    })


# ==========================================================
# RUN APPLICATION
# ==========================================================

if __name__ == "__main__":

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )