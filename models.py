from config import db

# Product Models
class Bag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    inspiration = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(100), nullable=False)
    # size = db.Column(db.String(50), nullable=False)  # Added size attribute

    def __repr__(self):
        return f'<Bag {self.name}>'

class Tshirt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    inspiration = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(100), nullable=False)
    # size = db.Column(db.String(50), nullable=False)  # Added size attribute

    def __repr__(self):
        return f'<Tshirt {self.name}>'

class Cap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    inspiration = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Cap {self.name}>'

# Order Model
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    customer_email = db.Column(db.String(100), nullable=False)
    order_items = db.relationship('OrderItem', back_populates='order', cascade='all, delete-orphan')  # One-to-Many

    def __repr__(self):
        return f'<Order {self.id} - {self.customer_name}>'

# OrderItem Model
class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_type = db.Column(db.String(50), nullable=False)  # 'Bag', 'Tshirt', or 'Cap'
    product_id = db.Column(db.Integer, nullable=False)  # ID of the specific product
    size = db.Column(db.String(50))  # Size (if applicable, e.g., Tshirts or Bags)
    quantity = db.Column(db.Integer, nullable=False, default=1)

    order = db.relationship('Order', back_populates='order_items')

    def __repr__(self):
        return f'<OrderItem {self.product_type} ID: {self.product_id}, Qty: {self.quantity}>'

