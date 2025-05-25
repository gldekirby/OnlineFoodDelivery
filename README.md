# Online Food Delivery Application

This project is a web application for online food delivery, built using Flask and MySQL. It allows users to register, log in, browse menu items, manage their cart, and place orders. Admins can manage menu items and view orders.

## Project Structure

- **src/app.py**: Main application logic for the Flask web app.
- **src/templates/**: Contains HTML templates for various pages:
  - **admin_dashboard.html**: Admin dashboard displaying orders and menu items.
  - **checkout.html**: Checkout page for finalizing orders.
  - **landing.html**: Landing page of the application.
  - **login.html**: Login page for user authentication.
  - **signup.html**: Signup page for new users.
  - **user_dashboard.html**: User dashboard displaying menu items and cart contents.
- **src/static/**: Contains static files for styling and client-side functionality.
  - **css/**: CSS files for styling the application.
  - **js/**: JavaScript files for client-side functionality.
- **database/schema.sql**: SQL schema defining the structure of the database.

## Setup Instructions

1. **Clone the repository**:
   ```
   git clone <repository-url>
   cd OnlineFoodDelivery
   ```

2. **Set up the database**:
   - Open your MySQL client and run the SQL commands in `database/schema.sql` to create the database and tables.

3. **Install dependencies**:
   - Make sure you have Python and pip installed. Then, install the required packages:
   ```
   pip install Flask mysql-connector-python bcrypt
   ```

4. **Run the application**:
   ```
   python src/app.py
   ```
   - The application will be available at `http://127.0.0.1:5000`.

## Usage

- **User Registration**: Navigate to the signup page to create a new account.
- **User Login**: Use the login page to access your account.
- **Browse Menu**: After logging in, you can view available menu items and add them to your cart.
- **Checkout**: Finalize your order by selecting a payment method on the checkout page.
- **Admin Dashboard**: Admin users can manage menu items and view all orders.

## License

This project is licensed under the MIT License.