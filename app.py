from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://your_username:your_password@localhost/grocery_store'
db = SQLAlchemy(app)

# Define Product model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(50), nullable=True)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    stock_quantity = db.Column(db.Integer, nullable=False)

# Define Customer model
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    phone_number = db.Column(db.String(20), nullable=True)

# Create tables
db.create_all()

# ... (rest of your code)

# Define routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_products', methods=['GET'])
def get_products():
    products = Product.query.all()
    products_data = [{'id': product.id, 'name': product.name, 'category': product.category,
                      'description': product.description, 'price': float(product.price),
                      'stock_quantity': product.stock_quantity} for product in products]
    return jsonify(products_data)

@app.route('/get_customers', methods=['GET'])
def get_customers():
    customers = Customer.query.all()
    customers_data = [{'id': customer.id, 'name': customer.name, 'email': customer.email,
                        'phone_number': customer.phone_number} for customer in customers]
    return jsonify(customers_data)

@app.route('/add_product', methods=['POST'])
def add_product():
    data = request.form
    product_name = data['productName']
    product_category = data['productCategory']
    product_description = data['productDescription']
    product_price = float(data['productPrice'])
    product_stock_quantity = int(data['productStockQuantity'])

    new_product = Product(name=product_name, category=product_category, description=product_description,
                          price=product_price, stock_quantity=product_stock_quantity)
    db.session.add(new_product)
    db.session.commit()

    return jsonify({'message': 'Product added successfully'})

@app.route('/add_customer', methods=['POST'])
def add_customer():
    data = request.form
    customer_name = data['customerName']
    customer_email = data['customerEmail']
    customer_phone_number = data['customerPhoneNumber']

    new_customer = Customer(name=customer_name, email=customer_email, phone_number=customer_phone_number)
    db.session.add(new_customer)
    db.session.commit()

    return jsonify({'message': 'Customer added successfully'})

if __name__ == '__main__':
    app.run(debug=True)
