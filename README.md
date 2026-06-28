# TechPrice — E-Commerce Price Tracker App

TechPrice is a modern, premium, glassmorphic (Frosted Liquid Glass) e-commerce price tracking web application. It allows users to browse trending tech products, view price changes, and track pricing history over time. It also features a secure, password-protected administrative dashboard for inventory management.

---

## 🚀 Key Features

* **Frosted Liquid Glass UI**: A visually rich dark-mode theme featuring organic drifting ambient layers, blurred backdrops, and interactive elements.
* **Scroll-Reveal Entrances**: Product cards animate in with smooth, staggered ease-out transitions as the user scrolls.
* **State Management**: Supports exact product states:
  * `In Stock` (renders prices and highlights discounts)
  * `Coming Soon` (displays coming soon badge)
  * `Out of Stock` (dimmed status, hides actions)
  * `Discontinued` (red warning tag)
* **Price History Graphs**: Interactive visual history charts mapping product price drops and shifts.
* **Admin Dashboard Control**: Full CRUD operation panels for adding, updating, and deleting products.
* **Argon2id Authentication**: Secure session-gated admin console using industrial-grade password hashing (via `argon2-cffi`).
* **First-Boot Auto-Seeding**: Checks database existence on launch and automatically seeds standard database items if missing.
* **Environment Configuration**: Robust `.env` variable control for ports, debug states, database URIs, and credentials.

---

## 🛠️ Technology Stack

* **Backend**: Flask 3.0, Flask-SQLAlchemy 3.1, SQLite
* **Security**: Argon2id (`argon2-cffi`)
* **Frontend**: HTML5, Vanilla JavaScript, CSS Custom Properties (Variables)
* **Configuration**: Python-dotenv 1.0

---

## 📋 Getting Started

### 1. Installation

Clone or navigate to the project directory and install python dependencies:
```bash
pip install -r requirements.txt
```

### 2. Configuration (`.env`)

Copy the production template to configure your local variables:
```bash
cp .env.example .env
```
Open `.env` and customize parameters like `SECRET_KEY`, `PORT`, `ADMIN_USERNAME`, or database path.

### 3. Database Seeding

Initialize and seed your database with sample tech products using the standalone seeder script:
```bash
python data_seeder.py
```

### 4. Running the App

Start the local Flask development server:
```bash
python app.py
```
By default, the server runs on [http://localhost:5000](http://localhost:5000).

---

## 🔐 Administrative Access

Navigate to `/admin` or click **Admin Console** in the navigation bar to login.

* **Default Username**: `admin`
* **Default Password**: `Admin@123`

---

## 📁 Project Structure

* `app.py` — Flask routes, controller APIs, and models
* `data_seeder.py` — Standalone script to initialize and populate initial products
* `static/`
  * `css/style.css` — Liquid glass styling guidelines and layouts
  * `js/main.js` — Landing interactions, mobile menus, and filter logic
  * `js/admin.js` — CRUD API requests, dynamic toast notifications, and stats updates
* `templates/`
  * `base.html` — Navigation bar, floating layers, and base HTML skeleton
  * `index.html` — Landing page with product grids and scroll reveals
  * `admin.html` — Admin table controls and modal forms
  * `login.html` — Session-gate login portal
  * `product_detail.html` — Interactive price charts and detail view
* `.env` / `.env.example` — Environment settings
