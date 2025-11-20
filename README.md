# 🪖 Olive Edge - E-Commerce Platform

[![Django](https://img.shields.io/badge/Django-5.2-green.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple.svg)](https://getbootstrap.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Premium Indian Army merchandise e-commerce platform built with Django. Shop for T-Shirts, Jackets, and Shirts celebrating the valor of the Indian Armed Forces.
---

## ✨ Features

### Customer Features
- 🛍️ **Product Catalog** - Browse T-Shirts, Jackets, and Shirts
- 🔍 **Category Filtering** - Filter products by category
- 🛒 **Shopping Cart** - Session-based cart for anonymous users
- 👤 **User Authentication** - Register, login, and profile management
- 📦 **Order Management** - Place orders and track order history
- 💳 **Checkout System** - Complete order placement with delivery details
- 📱 **Responsive Design** - Mobile-friendly Bootstrap interface

### Admin Features
- 📊 **Product Management** - Add, edit, delete products
- 📂 **Category Management** - Manage product categories
- 📋 **Order Tracking** - View and update order status
- 👥 **User Management** - Manage customer accounts
- 🖼️ **Image Upload** - Upload product images
- 📈 **Inventory Control** - Track stock levels

---

## Reference Screenshots

![Result](/static/media/products/2025/10/24/g1.png)
![Result](/static/media/products/2025/10/24/g3.png)
![Result](/static/media/products/2025/10/24/g2.png)

## 🛠️ Tech Stack

### Backend
- **Django 5.2** - Python web framework
- **SQLite** - Database (development)
- **Django ORM** - Object-Relational Mapping
- **Pillow** - Image processing

### Frontend
- **Bootstrap 5.3** - CSS framework
- **Django Templates** - Server-side rendering
- **HTML5 & CSS3** - Markup and styling
- **JavaScript** - Client-side interactivity

### Architecture
- **MVT Pattern** - Model-View-Template
- **Session-based Cart** - For anonymous users
- **Class-Based Views** - Reusable view components
- **Context Processors** - Global template variables

---

## 📁 Project Structure

```
oliveedge/
├── oliveedge/                 # Project configuration
│   ├── settings.py           # Django settings
│   ├── urls.py               # Main URL configuration
│   ├── wsgi.py               # WSGI configuration
│   └── asgi.py               # ASGI configuration
│
├── core/                      # Core app (homepage, about)
│   ├── views.py              # Home and static page views
│   ├── urls.py               # Core URL patterns
│   └── templates/core/       # Core templates
│
├── accounts/                  # User authentication
│   ├── views.py              # Login, register, profile views
│   ├── urls.py               # Account URL patterns
│   └── templates/accounts/   # Authentication templates
│
├── products/                  # Product catalog
│   ├── models.py             # Product and Category models
│   ├── views.py              # Product list and detail views
│   ├── admin.py              # Admin configuration
│   ├── urls.py               # Product URL patterns
│   └── templates/products/   # Product templates
│
├── cart/                      # Shopping cart
│   ├── cart.py               # Cart business logic
│   ├── views.py              # Cart views
│   ├── forms.py              # Cart forms
│   ├── context_processors.py # Cart context processor
│   ├── urls.py               # Cart URL patterns
│   └── templates/cart/       # Cart templates
│
├── orders/                    # Order management
│   ├── models.py             # Order and OrderItem models
│   ├── views.py              # Checkout and order views
│   ├── forms.py              # Order forms
│   ├── admin.py              # Order admin
│   ├── urls.py               # Order URL patterns
│   └── templates/orders/     # Order templates
│
├── templates/                 # Global templates
│   ├── base.html             # Base template
│   └── [app templates]       # App-specific templates
│
├── static/                    # Static files
│   ├── css/
│       └── style.css         # Custom styles 
│
├── media/                     # User uploads
│   └── products/             # Product images
│
├── db.sqlite3                 # SQLite database
├── manage.py                  # Django management script
└── README.md                  # This file
```

---

## 🚀 Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/oliveedge.git
cd oliveedge
```

### Step 2: Install Dependencies

```bash
pip install django pillow
```

### Step 3: Configure Database

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 5: Create Superuser

```bash
python manage.py createsuperuser
# Enter username, email, and password
```

### Step 6: Create Required Directories

```bash
# Windows
mkdir media\products
mkdir static\css

# macOS/Linux
mkdir -p media/products
mkdir -p static/css
```

### Step 7: Run Development Server

```bash
python manage.py runserver
```

Visit: **http://127.0.0.1:8000/**

---
