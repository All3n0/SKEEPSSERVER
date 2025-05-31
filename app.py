from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from flask_mail import Mail, Message
from config import create_app, db
from models import Order, OrderItem, Bag, Cap, Tshirt
from auth.admin_auth import require_admin

# Create app using factory
app = create_app()

# Add Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'skeepscollection@gmail.com'
app.config['MAIL_PASSWORD'] = 'fsdh ioze fyci lyus'  # App Password
app.config['MAIL_DEFAULT_SENDER'] = 'skeepscollection@gmail.com'

# Initialize extensions
mail = Mail(app)
CORS(app)


@app.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()

    customer_name = data.get("customer_name")
    customer_email = data.get("customer_email")
    instagram_handle = data.get("instagram_handle")
    items = data.get("items")

    if not (customer_name and customer_email and items):
        return jsonify({"error": "Missing customer details or items"}), 400

    # Store the Order in DB
    new_order = Order(
        customer_name=customer_name,
        customer_email=customer_email,
        instagram_handle=instagram_handle
    )
    db.session.add(new_order)
    db.session.flush()  # Get order.id before commit

    total_price = 0
    item_descriptions = []

    for item in items:
        order_item = OrderItem(
            order_id=new_order.id,
            product_name=item.get("product_name"),
            product_type=item.get("product_type"),
            quantity=item.get("quantity", 1)
        )
        db.session.add(order_item)

        # Track total price and prepare description
        try:
            item_price = float(item.get("price", 0))
            total_price += item_price
        except:
            item_price = 0  # fallback in case of bad data

        item_descriptions.append(f"{item.get('product_name')} - Ksh {item_price}")

    db.session.commit()

    # Send confirmation email
    try:
        msg = Message("Skeeps Collection Order Confirmation",
                      sender='skeepscollection@gmail.com',
                      recipients=[customer_email])
        msg.body = f"""
        Hello {customer_name},

        Thank you for placing an order with Skeeps Collection.

        Instagram: @{instagram_handle or 'N/A'}

        Items Ordered:
        {chr(10).join(item_descriptions)}

        Total: Ksh {total_price}

        We will reach out to you shortly with payment details.

        Regards,  
        Skeeps Collection
        """
        mail.send(msg)
    except Exception as e:
        print("Email failed:", e)

    return jsonify({"message": "Order created and email sent successfully"}), 201



@app.route('/orders', methods=['GET'])
def get_orders():
    orders = Order.query.all()
    result = [
        {
            "order_id": order.id,
            "customer_name": order.customer_name,
            "customer_email": order.customer_email,
            "instagram_handle": order.instagram_handle,
            "completed": order.completed,
            "items": [
                {
                    "product_type": item.product_type,
                    "product_name": item.product_name,
                    "quantity": item.quantity
                } for item in order.items
            ]
        } for order in orders
    ]
    return jsonify(result)
@app.route('/orders/<int:order_id>/complete', methods=['PATCH'])
def mark_order_complete(order_id):
    order = Order.query.get(order_id)
    if not order:
        return jsonify({"error": "Order not found"}), 404

    order.completed = True
    db.session.commit()
    return jsonify({"message": "Order marked as complete."})

@app.route('/orders/<int:order_id>/uncomplete', methods=['PATCH'])
def unmark_order_complete(order_id):
    order = Order.query.get(order_id)
    if not order:
        return jsonify({"error": "Order not found"}), 404
    order.completed = False
    db.session.commit()
    return jsonify({"message": "Order marked as incomplete"}), 200

@app.route('/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    order = Order.query.get(order_id)
    if not order:
        return jsonify({"error": "Order not found"}), 404

    db.session.delete(order)
    db.session.commit()
    return jsonify({"message": "Order deleted successfully!"})


# ----------------------- Bags -----------------------
@app.route('/bags', methods=['POST'])  # match the React endpoint
def create_bag():
    require_admin()
    data = request.get_json()

    new_bag = Bag(
        name=data['name'],
        price=data['price'],
        image=data['image'],
        inspiration=data.get('inspiration', '')
    )
    db.session.add(new_bag)
    db.session.commit()
    
    return jsonify({
        "message": "Bag created successfully!",
        "bag_id": new_bag.id
    }), 201

# @app.route('/bags', methods=['GET'])
# def get_bags():
#     bags = Bag.query.all()
#     result = [
#         {"id": b.id,"inspiration": b.inspiration,"name": b.name, "price": b.price, "image": b.image}
#         for b in bags
#     ]
#     return jsonify(result)

@app.route('/bags', methods=['GET'])
def get_inspirations():
    inspirations = (
        Bag.query.distinct(Bag.inspiration)
        .group_by(Bag.inspiration)
        .all()
    )
    result = [
        {
            "inspiration": b.inspiration,
            "image": b.image,  # Use the first image of this inspiration
        }
        for b in inspirations
    ]
    return jsonify(result)
@app.route('/bags/inspiration/<string:inspiration>', methods=['GET'])
def get_bags_by_inspiration(inspiration):
    bags = Bag.query.filter_by(inspiration=inspiration).all()
    result = [
        {
            "id": b.id,
            "name": b.name,
            "price": b.price,
            "image": b.image,
        }
        for b in bags
    ]
    return jsonify(result)

@app.route('/bags/<int:bag_id>', methods=['PUT'])
def update_bag(bag_id):
    data = request.get_json()
    bag_item = Bag.query.get(bag_id)
    if not bag_item:
        return jsonify({"error": "Bag not found"}), 404

    bag_item.name = data.get('name', bag_item.name)
    bag_item.price = data.get('price', bag_item.price)
    bag_item.image = data.get('image', bag_item.image)
    db.session.commit()
    return jsonify({"message": "Bag updated successfully!"})


@app.route('/bags/<int:bag_id>', methods=['DELETE'])
def delete_bag(bag_id):
    bag_item = Bag.query.get(bag_id)
    if not bag_item:
        return jsonify({"error": "Bag not found"}), 404

    db.session.delete(bag_item)
    db.session.commit()
    return jsonify({"message": "Bag deleted successfully!"})


# ----------------------- Caps -----------------------
@app.route('/caps', methods=['POST'])
def create_cap():
    data = request.get_json()
    if 'inspiration' not in data:
        return jsonify({"error": "Missing 'inspiration' key in request data"}), 400
    
    new_cap = Cap(
        name=data['name'],
        inspiration=data['inspiration'],
        price=data['price'],
        image=data['image']
    )
    db.session.add(new_cap)
    db.session.commit()
    return jsonify({"message": "Cap created successfully!", "cap_id": new_cap.id}), 201


@app.route('/caps', methods=['GET'])
def get_caps():
    caps = Cap.query.all()
    result = [
        {"id": c.id, "name": c.name, "price": c.price, "image": c.image}
        for c in caps
    ]
    return jsonify(result)


@app.route('/caps/<int:cap_id>', methods=['PUT'])
def update_cap(cap_id):
    data = request.get_json()
    cap_item = Cap.query.get(cap_id)
    if not cap_item:
        return jsonify({"error": "Cap not found"}), 404

    cap_item.name = data.get('name', cap_item.name)
    cap_item.price = data.get('price', cap_item.price)
    cap_item.image = data.get('image', cap_item.image)
    db.session.commit()
    return jsonify({"message": "Cap updated successfully!"})


@app.route('/caps/<int:cap_id>', methods=['DELETE'])
def delete_cap(cap_id):
    cap_item = Cap.query.get(cap_id)
    if not cap_item:
        return jsonify({"error": "Cap not found"}), 404

    db.session.delete(cap_item)
    db.session.commit()
    return jsonify({"message": "Cap deleted successfully!"})


# ----------------------- T-Shirts -----------------------
@app.route('/tshirts', methods=['POST'])
def create_tshirt():
    require_admin()
    data = request.get_json()
    new_tshirt = Tshirt(
        name=data['name'],
        inspiration=data['inspiration'],  # Add this line
        price=data['price'],
        image=data['image']
    )
    db.session.add(new_tshirt)
    db.session.commit()
    return jsonify({"message": "T-Shirt created successfully!", "tshirt_id": new_tshirt.id}), 201

@app.route('/tshirts', methods=['GET'])
def get_tshirt_inspirations():
    inspirations = (
        Tshirt.query.distinct(Tshirt.inspiration)
        .group_by(Tshirt.inspiration)
        .all()
    )
    result = [
        {
            "inspiration": t.inspiration,
            "image": t.image,  # Use the first image of this inspiration
        }
        for t in inspirations
    ]
    return jsonify(result)

@app.route('/tshirts/inspiration/<string:inspiration>', methods=['GET'])
def get_tshirts_by_inspiration(inspiration):
    tshirts = Tshirt.query.filter_by(inspiration=inspiration).all()
    result = [
        {
            "id": t.id,
            "name": t.name,
            "price": t.price,
            "image": t.image,
        }
        for t in tshirts
    ]
    return jsonify(result)



@app.route('/tshirts/<int:tshirt_id>', methods=['PUT'])
def update_tshirt(tshirt_id):
    data = request.get_json()
    tshirt_item = Tshirt.query.get(tshirt_id)
    if not tshirt_item:
        return jsonify({"error": "T-Shirt not found"}), 404

    tshirt_item.name = data.get('name', tshirt_item.name)
    tshirt_item.price = data.get('price', tshirt_item.price)
    tshirt_item.image = data.get('image', tshirt_item.image)
    db.session.commit()
    return jsonify({"message": "T-Shirt updated successfully!"})


@app.route('/tshirts/<int:tshirt_id>', methods=['DELETE'])
def delete_tshirt(tshirt_id):
    tshirt_item = Tshirt.query.get(tshirt_id)
    if not tshirt_item:
        return jsonify({"error": "T-Shirt not found"}), 404

    db.session.delete(tshirt_item)
    db.session.commit()
    return jsonify({"message": "T-Shirt deleted successfully!"})
@app.route('/all_bags', methods=['GET'])
def get_all_bags():
    bags = Bag.query.all()
    return jsonify([bag.to_dict() for bag in bags]), 200

@app.route('/all_tshirts', methods=['GET'])
def get_all_tshirts():
    tshirts = Tshirt.query.all()
    return jsonify([tshirt.to_dict() for tshirt in tshirts]), 200
# Flask route
from sqlalchemy import or_

@app.route('/search')
def search():
    query = request.args.get('q', '').lower()

    bags = Bag.query.filter(
        or_(
            Bag.name.ilike(f'%{query}%'),
            Bag.inspiration.ilike(f'%{query}%')
        )
    ).all()

    tshirts = Tshirt.query.filter(
        or_(
            Tshirt.name.ilike(f'%{query}%'),
            Tshirt.inspiration.ilike(f'%{query}%')
        )
    ).all()

    return jsonify({
        'bags': [bag.to_dict() for bag in bags],
        'tshirts': [tshirt.to_dict() for tshirt in tshirts]
    })
@app.route('/')
def index():
    return "Yee,skeeps!"


if __name__ == '__main__':
    app.run(debug=True)
