# Eshop - Ecommerce Web Application

## Overview
Eshop is a modern, scalable, and feature-rich e-commerce web application built using Django. It enables users to seamlessly browse products, manage their carts, and complete purchases. The platform is designed with a secure authentication system, an efficient order management process, and a powerful admin panel for managing products and transactions.

## Features
- **User Authentication**: Secure signup, login, and logout functionalities.
- **Product Management**: Categorization, detailed product descriptions, and search capabilities.
- **Shopping Cart & Checkout**: Add items to cart, modify quantities, and proceed to checkout.
- **Order Management**: View order history, track shipments, and receive email confirmations.
- **Admin Dashboard**: Manage products, orders, and users with an intuitive interface.
- **Mobile-Responsive Design**: Ensuring a seamless experience on all devices.
- **Secure Payment Integration**: (Future Implementation)

## Technologies Used
- **Backend**: Django, Django REST Framework
- **Frontend**: HTML, CSS, Bootstrap, JavaScript
- **Database**: SQLite (Easily switchable to PostgreSQL or MySQL)
- **Deployment**: PythonAnywhere, GitHub, AWS (Future Deployment)

## Installation Guide

### 1. Clone the Repository
```bash
git clone https://github.com/lisaluck/ecomwebshoop.git
cd ecomwebshoop
```

### 2. Create and Activate a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Required Dependencies
```bash
pip install -r requirements.txt
```

### 4. Apply Migrations and Create Superuser
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 5. Run the Development Server
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000/` in your browser.

## Deployment Guide (PythonAnywhere)
1. Upload project files to PythonAnywhere.
2. Set up a virtual environment and install dependencies.
3. Configure the `WSGI` file for Django.
4. Update static files settings and run migrations.

## Folder Structure
```
Eshop/
│── eshop/ (Main Django Project)
│── limma/ (Custom Ecommerce App)
│── templates/ (HTML Templates)
│── static/ (CSS, JavaScript, Images)
│── db.sqlite3 (Database)
│── manage.py (Django Management Script)
│── requirements.txt (Project Dependencies)
│── README.md (Project Documentation)
```

## License
This project is licensed under the **MIT License**. Feel free to contribute and enhance its functionality.

