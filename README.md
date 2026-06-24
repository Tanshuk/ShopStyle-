# 🛍️ ShopStyle - Fashion E-Commerce Platform

<div align="center">




\

A modern fashion e-commerce platform inspired by leading online shopping websites. Built using **Django**, featuring secure authentication, product management, shopping cart, wishlist, order management, and a responsive user interface.

</div>

---

# ✨ Features

### 👤 User Authentication

* User Registration & Login
* Secure Logout
* Password Reset
* User Profile Management
* Change Password

### 🛍️ Shopping

* Product Categories
* Product Search
* Product Details
* Multiple Product Images
* Wishlist
* Shopping Cart
* Quantity Management
* Order Checkout

### 📦 Order Management

* Place Orders
* Order History
* Order Status Tracking
* Invoice Generation

### 💳 Payment

* Cash on Delivery
* Online Payment Integration (Planned)

### ⭐ Reviews

* Product Ratings
* Customer Reviews

### ⚙️ Admin Dashboard

* Manage Products
* Manage Categories
* Manage Brands
* Manage Orders
* Manage Users
* Inventory Management

---

# 🛠 Tech Stack

| Category       | Technology                                    |
| -------------- | --------------------------------------------- |
| Backend        | Django, Python                                |
| Frontend       | HTML5, CSS3, Bootstrap 5, JavaScript          |
| Database       | SQLite (Development), PostgreSQL (Production) |
| Authentication | Django Authentication System                  |
| Image Handling | Pillow                                        |
| Deployment     | Gunicorn, WhiteNoise                          |

---

# 📂 Project Structure

```text
shopstyle/
│
├── accounts/
├── core/
├── products/
├── cart/
├── wishlist/
├── orders/
├── payments/
├── reviews/
├── dashboard/
│
├── templates/
├── static/
├── media/
│
├── manage.py
├── requirements.txt
└── README.md
```

---

# 🗄️ Database Models

* User
* Category
* Brand
* Product
* Product Image
* Cart
* Cart Item
* Wishlist
* Order
* Order Item
* Payment
* Review
* Address

---

# 🚀 Installation

Clone the repository

```bash
git clone https://github.com/TanshuK/shopstyle.git
cd shopstyle
```

Create a virtual environment

```bash
python -m venv venv
```

Activate the environment

**Linux / macOS**

```bash
source venv/bin/activate
```

**Windows**

```bash
venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Apply migrations

```bash
python manage.py migrate
```

Create a superuser

```bash
python manage.py createsuperuser
```

Run the development server

```bash
python manage.py runserver
```

Visit:

```
http://127.0.0.1:8000/
```

---

# ⚙️ Environment Variables

Create a `.env` file.

```env
SECRET_KEY=your_secret_key
DEBUG=True

EMAIL_HOST=
EMAIL_PORT=
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=

DATABASE_URL=
```

---

# 🎯 Current Progress

* ✅ Authentication System
* ✅ Homepage
* ✅ Responsive UI
* 🚧 Products Module
* 🚧 Shopping Cart
* 🚧 Wishlist
* 🚧 Checkout
* 🚧 Payment Integration
* 🚧 Admin Dashboard

---

# 🛣️ Future Enhancements

* Razorpay Integration
* Stripe Integration
* Coupon System
* Product Recommendations
* Email Notifications
* REST API
* Docker Support
* Dark Mode
* Product Analytics

---

# 📄 License

This project is licensed under the MIT License.

---

# 👨‍💻 Developer

**Tanshu Gautam**

* GitHub: https://github.com/TanshuK
* LinkedIn: https://www.linkedin.com/in/tanshu-kumar-597b3a32b/

---

⭐ If you found this project useful, consider giving it a star.
