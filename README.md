# Django Store Project

## Overview
This project is a full-stack e-commerce store built with Django and Django Rest Framework (DRF) for the backend and a separate frontend using HTML, Bootstrap, and vanilla JavaScript with Axios for API communication. The frontend and backend are completely separated and communicate through a RESTful API.

## Features
- **User Registration & OTP Verification:**  
  Users register with email, username, and password. An OTP is sent (using Celery and Redis) for verification before logging in.
  
- **User Login & JWT Authentication:**  
  Users log in to receive JWT access and refresh tokens. The tokens are stored in localStorage and used for subsequent authenticated API requests.
  
- **User Dashboard:**  
  Users can view and update their profile (first name, last name, phone number) and manage their addresses. Addresses are handled as a separate model linked to the user.
  
- **Product Listing & Filtering:**  
  The API supports filtering products by category, price ranges, and supports sorting. It uses Django Filters for query parameter-based filtering.
  
- **Cart Functionality:**  
  The shopping cart is stored as a dictionary in localStorage containing product IDs and quantities. The cart page fetches product details from the API, validates quantities against stock, and allows users to adjust item quantities.
  
- **Order Management & Coupons:**  
  Orders, order products, and coupons are implemented using Django models. Orders link to users and contain order items with discount details.
  
- **Asynchronous Tasks:**  
  Celery is integrated with Redis to handle time-consuming tasks such as sending OTP emails without blocking the main application workflow.
  
- **Environment Variables for Security:**  
  Sensitive information (e.g., email credentials, secret keys) are stored in environment variables and loaded using `python-dotenv`.

- **Payment:**
  Payments are done using Zarinpal sandbox and are validated in backend

## Architecture
- **Backend:**  
  - **Django & DRF:** Serves a RESTful API for products, user profiles, addresses, orders, and authentication.
  - **SimpleJWT:** Provides JWT-based authentication.
  - **Celery & Redis:** Used for sending OTP emails asynchronously.
  - **Django Filters:** Allows filtering and ordering of API data.
  
- **Frontend:**  
  - **HTML & Bootstrap:** Provide a responsive and user-friendly interface.
  - **Vanilla JavaScript & Axios:** Handle API calls and dynamic DOM updates (e.g., for the cart and user dashboard).
  - **LocalStorage:** Used to store the shopping cart and JWT tokens.
  
- **Database:**  
  Utilizes Django’s ORM with models for `Feature`, `Discount`, `Product`, `Coupon`, `Order`, `OrderProduct`, `CustomUser` (inherited from `AbstractUser`), and `Address`.

## Setup Instructions

### Prerequisites
- Python 3.10+
- Django 5.1+
- Redis server
- Celery


### Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/mahdimon/final_project.git
   cd final_project

2. **Create a Virtual Environment and Activate It:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt

4. **Set Up Environment Variables: Create a .env file in the project root (at the same level as manage.py)**
   ```bash
   SECRET_KEY=your_secret_key
   DEBUG=True
   EMAIL_HOST_USER=your_email@example.com
   EMAIL_HOST_PASSWORD=your_email_password

5. **Make and Run Migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate

6. **Start Redis Server:**
   ```bash
   redis-server

7. **Start the Celery Worker:**
   ```bash
   celery -A store --loglevel=info

8. **Run the Django Development Server:**
   ```bash
   python manage.py runserver

