from config import db

# Product Models
class Bag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    inspiration = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(100), nullable=False)
    # size = db.Column(db.String(50), nullable=False)  # Added size attribute
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'image': self.image,
            'inspiration': self.inspiration
        }

    def __repr__(self):
        return f'<Bag {self.name}>'

class Tshirt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    inspiration = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(100), nullable=False)
    # size = db.Column(db.String(50), nullable=False)  # Added size attribute
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'image': self.image,
            'inspiration': self.inspiration
        }
    def __repr__(self):
        return f'<Tshirt {self.name}>'

class Hoodie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    inspiration = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Hoodie {self.name}>'

# Order Model
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String)
    customer_email = db.Column(db.String)
    instagram_handle = db.Column(db.String)  # <- Add this if not there
    completed = db.Column(db.Boolean, default=False)  # <- For marking complete
    items = db.relationship('OrderItem', backref='order', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'customer_name': self.customer_name,
            'customer_email': self.customer_email,
            'instagram_handle': self.instagram_handle,
            'completed': self.completed,
            'items': [item.to_dict() for item in self.items]
        }
class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_type = db.Column(db.String)
    product_name = db.Column(db.String)  # <- Add this if you want name
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))

    def to_dict(self):
        return {
            'id': self.id,
            'product_type': self.product_type,
            'product_name': self.product_name,
            'quantity': self.quantity,
            'price': self.price
        }


