# PROJECT_9__DJANGO_LITReview

## Project Description

This project is a web application built with Django that allows users to create tickets and reviews. Users can also follow other users and see their activities on their feed.

## Installation

1. Clone this repository to your local machine using the following command:
   ```bash
   git clone https://github.com/samichelly/P9__Django_web_app.git
   ```
2. Navigate to the project directory:
   ```bash
   cd P9__Django_web_app\LITReview
   ```
3. Create a virtual environment to isolate dependencies:
   ```bash
   python -m venv venv
   ```
4. Activate the virtual environment (depending on your operating system):
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```bash
     source venv/bin/activate
     ```
5. Install the dependencies from the `requirements.txt` file:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Start the Django development server:
   ```bash
   python manage.py runserver
   ```
2. Access the application from your preferred browser at:
   ```text
   http://127.0.0.1:8000/
   ```
3. You can now sign up, log in, create tickets, write reviews, follow other users, and interact with each other.

## Creating a New User

To create a new user, follow these steps:
1. Go to the application's sign-up page at:
   ```text
   http://127.0.0.1:8000/signup
   ```
2. Fill out the registration form with your information, such as username, email address, and password.
3. Click the "Submit" button to submit the form.
4. Once the form is successfully submitted, you will be redirected to the login page.
5. Use your credentials to log in to the application.

## User Accounts

- **User 1:**
  - Username: lecteur1
  - Password: litreview

- **User 2:**
  - Username: lecteur2
  - Password: litreview

## Django Administration

- **Admin Account:**
  - Username: Admin
  - Password: litreview

Access the admin panel at:
```text
http://127.0.0.1:8000/admin/
```
