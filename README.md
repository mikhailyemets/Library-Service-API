# Library API Service


![Django REST Framework](https://www.django-rest-framework.org/img/logo.png)
<img src="https://uxwing.com/wp-content/themes/uxwing/download/brands-and-social-media/docker-icon.png" alt="Docker" width="120">
![Stripe](https://upload.wikimedia.org/wikipedia/commons/thumb/b/ba/Stripe_Logo%2C_revised_2016.svg/120px-Stripe_Logo%2C_revised_2016.svg.png)
![Telegram Bot](https://upload.wikimedia.org/wikipedia/commons/thumb/8/82/Telegram_logo.svg/120px-Telegram_logo.svg.png)
<img src="https://miro.medium.com/v2/resize:fit:1000/1*ebqXeX88dFY9FWbFIvMfHw.png" alt="Celery" width="240">
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
___

### About The Project

#### **This project provides a comprehensive set of endpoints to manage the entire library ecosystem. The online management system for book borrowings aims to revolutionize the library's operations. The service offers the following features:**

* Browse Inventory: Users can browse the library's inventory and select the books they want to borrow.

* Track Borrowed Items: Users can keep track of their borrowed items and due dates.

* Online Payments: Users have the option to pay for their borrowings online, eliminating the need for cash transactions.

# Installation
1. **Clone the repository:**

   ```sh
   git clone https://github.com/mikhailyemets/Library-Service-API.git
   cd library_service

2. Create and activate **venv** (bash):
   ```sh
   python -m venv venv
   source venv/Scripts/activate
   ```
   Windows (Command Prompt)
   ```sh
   python -m venv venv
   venv\Scripts\activate
   ```
   Mac / Linux (Unix like systems)
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```
   
3. Create an `.env` file in the root of the project directory. You can use the `.env.example` file as a template (just change DJANGO_SECRET_KEY):
    ```sh
    cp .env.example .env
    ```
   
### Local installation:
1. Install **requirements.txt** to your **venv**:
   ```sh
   pip install -r requirements.txt
   ```
 
2. Create apply migrations:
   ```sh
   python manage.py migrate
   ```
   
3. (Optional) use my sample of prefilled DB:
   ```sh
   python manage.py fill_authors
   python manage.py fill_books
   ```
   
4. Start the server:
   ```sh
   python manage.py runserver
   ```
   
### The API will now be accessible at http://localhost:8000/

##### For creating user you should:
1. Go to one of these link:
   - Register user: /users/register
   - Get token: /users/token

### Token Management
- Refresh your token when it expires using the following URL: /users/token/refresh
- Get information about yourself using the following URL: //localhost:8000/users/token/me

   
### Docker local installation:
1. Create app image and start it:
   ```sh
   docker-compose build
   docker-compose up
   ```
 
### If you used prefilled database from .json:
   - **admin_user**. email: admin@mail.com, password: 123123
   - **auth_user**. email: user@mail.com, password: 123123

## Important Endpoints in Project:

##### * /api/books/ - Assortment of books
##### * /api/authors/ - Available authors
##### * /api/borrowings/ - Book rental service
##### * /api/payments/ - Book payment service
##### * /api/user/ - User page
For detailed API documentation, visit [Swagger Documentation](http://localhost:8000/api/doc/swagger/).


## Key Features

- **JWT authenticated**

- **Automated Tracking**
  - Tracks borrowed books and due dates.
  - Sends notifications to users about due dates and overdue books.

- **User Notifications**
  - Provides timely updates on borrowed items.
  - Users receive alerts when items are due or overdue.

- **Real-Time Data for Administrators**
  - Access to up-to-date information on borrowed items and user accounts.
  - Enhances efficiency for both users and library administrators.

- **Payment Management**
  - Allows users to make payments for borrowed items or fines.
  - Supports payment status tracking (Pending, Paid).
  - Provides session URLs and IDs for payment processing.
