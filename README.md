# LocalSync — Bharat Edition

**LocalSync** is a lightweight, vernacular-first Customer Relationship Management (CRM) and **Adaptive Restock Engine** built to help local Indian Kirana stores compete with quick-commerce apps. Instead of waiting for customers to reorder manually or spamming them on rigid schedules, LocalSync tracks household consumption cycles and triggers personalized, multi-lingual restock prompts.

---

## Key Features

### 1. Adaptive Restock Engine
* **Consumption Cycle Tracking:** Automatically tracks purchase intervals (`cycle_days`) per customer-product pair and flags items due for restock.
* **Self-Adjusting Feedback Loop:** Learns from customer responses in real time:
  * **Option 1 (Place Order):** Generates a pending delivery order and resets the reminder timer.
  * **Option 2 (Self Pickup):** Creates a store pickup order with an automatic ₹10 discount incentive.
  * **Option 3 (Still Have Stock):** Extends the customer's consumption cycle by **+5 days**, pushes the next reminder date forward, and logs the adjustment in `reminder_logs`.

### 2. Multi-Lingual Customer & Merchant Support
* **Regional Customer Messaging:** Sends restock prompts and interactive reply options in the customer's saved preferred language (**Hindi, Malayalam, Kannada, Telugu, Tamil, Marathi, Bengali, Gujarati, and English**).
* **Vernacular Shopkeeper Dashboard:** Allows store owners to switch the entire workspace interface into their preferred regional language with persistent `localStorage` state.

### 3. Interactive WhatsApp Chat Simulator
* Built-in mobile WhatsApp preview modal allowing live end-to-end testing of customer reorder flows without requiring external API credentials during local development.
* Decoupled `/api/reminders/<id>/respond` backend architecture ready to connect directly to **Meta WhatsApp Cloud API** or **Twilio** webhooks.

### 4. Store Operations & Inventory Management
* **Live Store Overview:** Real-time metrics for active customers, tracked inventory items, pending orders, and due restocks.
* **Customer Directory:** Searchable customer database enforcing unique phone numbers and preferred regional language tags.
* **Product Catalog:** Category-based inventory tracking with stock levels, units (`bag`, `pack`, `bottle`, `packet`), and pricing.
* **Order Queue:** Automated order generation (`#LS-XXXX`) tracking fulfilment mode (`Delivery` vs. `Self Pickup`) and order status.

---

## Tech Stack

* **Backend:** Python 3, Flask 3.1.2
* **Database:** SQLite3 with foreign-key enforcement (`PRAGMA foreign_keys = ON`) and cascading deletes
* **Frontend:** HTML5 (Jinja2 templates), Vanilla CSS3 (Responsive Grid/Flexbox), Vanilla JavaScript (ES6+ Fetch API)

---

## Database Schema

LocalSync uses a 5-table relational SQLite schema (`localsync.db`):
1. `customers` — Customer profiles, unique phone numbers, addresses, and preferred languages.
2. `products` — Store catalog, categories, unit pricing, and available stock.
3. `customer_products` — Tracks per-customer consumption cycles, last purchase dates, next reminder dates, and snooze counts.
4. `orders` — Stores delivery and self-pickup orders generated from customer interactions.
5. `reminder_logs` — Audit trail recording customer responses and old-to-new cycle adjustments.

---

## Getting Started

### Prerequisites
* Python 3.9+

### Installation & Run
1. **Clone the repository:**
   ```bash
   git clone [https://github.com/](https://github.com/)<your-username>/localsync.git
   cd localsync

 2. Install dependencies-
 ' pip install -r requirements.txt '

 3. Run the application-
    python app.py

 4. Open in browser:
    Navigate to http://127.0.0.1:5000   
