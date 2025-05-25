import os
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, send_from_directory
import mysql.connector
from bcrypt import hashpw, gensalt, checkpw
from werkzeug.utils import secure_filename
import decimal

from enum import Enum

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

class CategoryEnum(Enum):
    PREMIUM = "Premium"
    STEAK = "Steak"
    RICE_REAL = "Rice Meal"
    FAMILY_MEAL = "Family Meal"
    SNACKS = "Snacks"
    HOUSE_SPECIALTY = "House Specialty"
    SPECIAL_OFFER_VJS_SHAWARMA = "Special Offer Vj's Shawarma"

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limit file size to 16MB

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'food_delivery'
}

def get_db_connection():
    connection = mysql.connector.connect(**db_config)
    connection.autocommit = True
    return connection

@app.route('/')
def home():
    return redirect(url_for('view_menu'))

@app.route('/menu', methods=['GET'])
def view_menu():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM menu")
    menu_items = cursor.fetchall()
    cursor.close()
    connection.close()

    # Handle missing photo_path by providing a default placeholder image
    for item in menu_items:
        if not item.get('photo_path'):
            item['photo_path'] = 'static/images/placeholder.png'

    # Group menu items by category
    grouped_menu = {}
    for item in menu_items:
        category = item.get('category', 'Uncategorized')
        if category not in grouped_menu:
            grouped_menu[category] = []
        grouped_menu[category].append(item)

    return render_template('menu.html', menu=grouped_menu)

@app.route('/order', methods=['POST'])
def place_order():
    order_details = request.json
    connection = get_db_connection()
    cursor = connection.cursor()

    # Insert order into the database
    cursor.execute("INSERT INTO orders (status, order_date) VALUES ('Pending', NOW())")
    order_id = cursor.lastrowid

    # Insert order items into the database
    for item in order_details['items']:
        cursor.execute(
            "INSERT INTO order_items (order_id, item_id, quantity) VALUES (%s, %s, %s)",
            (order_id, item['menu_item_id'], item['quantity'])
        )

    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({'message': 'Order placed successfully', 'order_id': order_id})

@app.route('/admin/dashboard')
def admin_dashboard():
    return redirect(url_for('admin_menu'))

@app.route('/admin/menu')
def admin_menu():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT id, name, description, price, photo_path, category, status FROM menu")
    menu_items = cursor.fetchall()

    for item in menu_items:
        if not item.get('photo_path'):
            item['photo_path'] = 'static/images/placeholder.png'

    cursor.close()
    connection.close()

    return render_template('admin_menu.html', menu=menu_items)

@app.route('/admin/orders')
def admin_orders():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT o.id AS order_id, o.order_date, o.status, m.id AS menu_id, m.name AS item_name, oi.quantity, m.price
        FROM orders o
        JOIN order_items oi ON o.id = oi.order_id
        JOIN menu m ON oi.item_id = m.id
        ORDER BY o.order_date DESC
        """
    )
    flat_orders = cursor.fetchall()

    orders_dict = {}
    for row in flat_orders:
        order_id = row['order_id']
        if order_id not in orders_dict:
            orders_dict[order_id] = {
                'order_id': order_id,
                'order_date': row['order_date'],
                'status': row['status'],
                'items': [],
                'total_amount': decimal.Decimal(0)
            }
        item_total = decimal.Decimal(row['price']) * row['quantity']
        orders_dict[order_id]['items'].append({
            'item_name': row['item_name'],
            'quantity': row['quantity'],
            'price': row['price'],
            'item_total': item_total
        })
        orders_dict[order_id]['total_amount'] += item_total

    orders = list(orders_dict.values())

    cursor.close()
    connection.close()

    return render_template('admin_orders.html', orders=orders)

@app.route('/admin/menu/add', methods=['POST'])
def add_menu_item():
    try:
        # Check if the photo file is in the request
        if 'photo' not in request.files:
            app.logger.error("Photo file is missing in the request.")
            return jsonify({'error': 'Photo file is required'}), 400

        file = request.files['photo']
        if file.filename == '':
            app.logger.error("No file selected for upload.")
            return jsonify({'error': 'No selected file'}), 400

        # Secure the filename and save the file to the uploads directory
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Collect form data
        new_item = {
            'name': request.form.get('name'),
            'description': request.form.get('description'),
            'price': request.form.get('price'),
            'photo_path': filename,
            'category': request.form.get('category'),
            'status': request.form.get('status', 'available')
        }

        # Validate that all fields are provided
        missing_fields = [key for key, value in new_item.items() if not value]
        if missing_fields:
            app.logger.error(f"Missing fields: {missing_fields}")
            return jsonify({'error': f'Missing fields: {missing_fields}'}), 400

        # Validate category against enum
        if new_item['category'] not in [cat.value for cat in CategoryEnum]:
            app.logger.error(f"Invalid category: {new_item['category']}")
            return jsonify({'error': f"Invalid category: {new_item['category']}"}), 400

        # Validate status
        if new_item['status'] not in ['available', 'not available']:
            app.logger.error(f"Invalid status: {new_item['status']}")
            return jsonify({'error': f"Invalid status: {new_item['status']}"}), 400

        # Insert the new menu item into the database
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO menu (name, description, price, photo_path, category, status) VALUES (%s, %s, %s, %s, %s, %s)",
            (new_item['name'], new_item['description'], new_item['price'], new_item['photo_path'], new_item['category'], new_item['status'])
        )
        connection.commit()
        cursor.close()
        connection.close()

        app.logger.info("Menu item added successfully.")
        return jsonify({'message': 'Menu item added successfully'})
    except mysql.connector.Error as err:
        app.logger.error(f"Database error: {err}")
        return jsonify({'error': f'Database error: {err}'}), 500
    except Exception as e:
        app.logger.error(f"Unexpected error: {e}")
        return jsonify({'error': f'An unexpected error occurred: {e}'}), 500

from flask import request

@app.route('/admin/menu/update', methods=['POST'])
def update_menu_item():
    if 'photo' in request.files:
        file = request.files['photo']
        if file.filename != '':
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
        else:
            filename = None
    else:
        filename = None

    item_id = request.form.get('id')
    if not item_id:
        return jsonify({'error': 'Item ID is required'}), 400

    # Prepare fields to update
    fields = []
    values = []

    # Optional fields
    name = request.form.get('name')
    if name is not None:
        fields.append('name = %s')
        values.append(name)

    price = request.form.get('price')
    if price is not None:
        fields.append('price = %s')
        values.append(price)

    description = request.form.get('description')
    if description is not None:
        fields.append('description = %s')
        values.append(description)

    category = request.form.get('category')
    if category is not None:
        # Validate category against enum
        if category not in [cat.value for cat in CategoryEnum]:
            return jsonify({'error': f"Invalid category: {category}"}), 400
        fields.append('category = %s')
        values.append(category)

    status = request.form.get('status')
    if status is not None:
        # Validate status
        if status not in ['available', 'not available']:
            return jsonify({'error': f"Invalid status: {status}"}), 400
        fields.append('status = %s')
        values.append(status)

    if filename:
        fields.append('photo_path = %s')
        values.append(filename)

    if not fields:
        return jsonify({'error': 'No fields to update'}), 400

    values.append(item_id)

    query = f"UPDATE menu SET {', '.join(fields)} WHERE id = %s"

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(query, tuple(values))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({'message': 'Menu item updated successfully'})

@app.route('/admin/menu/delete', methods=['DELETE'])
def delete_menu_item():
    item_id = request.json['id']
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM menu WHERE id = %s", (item_id,))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({'message': 'Menu item deleted successfully'})

@app.route('/admin/menu/bulk_delete', methods=['POST'])
def bulk_delete_menu_items():
    ids = request.json.get('ids', [])
    if not ids:
        return jsonify({'error': 'No item IDs provided'}), 400

    connection = get_db_connection()
    cursor = connection.cursor()
    format_strings = ','.join(['%s'] * len(ids))
    query = f"DELETE FROM menu WHERE id IN ({format_strings})"
    cursor.execute(query, tuple(ids))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({'message': f'{len(ids)} menu items deleted successfully'})

@app.route('/admin/order/update_status', methods=['POST'])
def update_order_status():
    data = request.json
    order_id = data.get('order_id')
    new_status = data.get('status')

    if new_status not in ['Pending', 'Preparing', 'Ready', 'Completed', 'Cancelled']:
        return jsonify({'error': 'Invalid status value'}), 400

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE orders SET status = %s WHERE id = %s", (new_status, order_id))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({'message': 'Order status updated successfully'})

@app.route('/admin/order/add', methods=['POST'])
def add_order():
    order_details = request.json
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        connection.start_transaction()
        # Calculate total amount for the order
        total_amount = 0
        for item in order_details['items']:
            cursor.execute("SELECT price FROM menu WHERE id = %s", (item['menu_item_id'],))
            price_result = cursor.fetchone()
            price = price_result[0] if price_result else 0
            total_amount += price * item['quantity']

        # Insert order into the database with total amount
        cursor.execute("INSERT INTO orders (status, amount) VALUES ('Pending', %s)", (total_amount,))
        order_id = cursor.lastrowid

        # Insert order items into the database without amount
        for item in order_details['items']:
            cursor.execute(
                "INSERT INTO order_items (order_id, item_id, quantity) VALUES (%s, %s, %s)",
                (order_id, item['menu_item_id'], item['quantity'])
            )

        connection.commit()
        return jsonify({'message': 'Order added successfully', 'order_id': order_id})
    except mysql.connector.Error as err:
        connection.rollback()
        app.logger.error(f"Database error during order placement: {err}")
        return jsonify({'error': 'Failed to place order due to database error.'}), 500
    except Exception as e:
        connection.rollback()
        app.logger.error(f"Unexpected error during order placement: {e}")
        return jsonify({'error': 'Failed to place order due to unexpected error.'}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/admin/menu/upload', methods=['POST'])
def upload_photo():
    if 'photo' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['photo']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({'message': 'File uploaded successfully', 'photo_path': filename})

# Route to serve uploaded files
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/api/menu/status', methods=['GET'])
def api_menu_status():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT id, status FROM menu")
    menu_statuses = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(menu_statuses)

from flask import jsonify

@app.route('/api/menu', methods=['GET'])
def api_menu():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM menu")
    menu_items = cursor.fetchall()
    cursor.close()
    connection.close()

    # Group menu items by category
    grouped_menu = {}
    for item in menu_items:
        category = item.get('category', 'Uncategorized')
        if category not in grouped_menu:
            grouped_menu[category] = []
        grouped_menu[category].append(item)

    return jsonify(grouped_menu)

if __name__ == '__main__':
    app.run(debug=True)
