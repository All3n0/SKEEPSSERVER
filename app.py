from flask import Flask, request, jsonify
from config import create_app, db
from models import Order, OrderItem, bag, cap, tshirt
from flask_cors import CORS

app = Flask(__name__)
app = create_app()
CORS(app)

# ----------------------- Orders -----------------------
@app.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    new_order = Order(
        customer_name=data['customer_name'],
        customer_email=data['customer_email']
    )
    db.session.add(new_order)

    for item in data['items']:
        order_item = OrderItem(
            order=new_order,
            product_type=item['product_type'],
            product_id=item['product_id'],
            size=item.get('size'),  # Optional
            quantity=item['quantity']
        )
        db.session.add(order_item)

    db.session.commit()
    return jsonify({"message": "Order created successfully!", "order_id": new_order.id}), 201


@app.route('/orders', methods=['GET'])
def get_orders():
    orders = Order.query.all()
    result = [
        {
            "order_id": order.id,
            "customer_name": order.customer_name,
            "customer_email": order.customer_email,
            "items": [
                {
                    "product_type": item.product_type,
                    "product_id": item.product_id,
                    "size": item.size,
                    "quantity": item.quantity
                } for item in order.order_items
            ]
        } for order in orders
    ]
    return jsonify(result)


@app.route('/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    order = Order.query.get(order_id)
    if not order:
        return jsonify({"error": "Order not found"}), 404

    db.session.delete(order)
    db.session.commit()
    return jsonify({"message": "Order deleted successfully!"})


# ----------------------- Bags -----------------------
@app.route('/bags', methods=['POST'])
def create_bag():
    data = request.get_json()
    new_bag = bag(
        name=data['name'],
        price=data['price'],
        image=data['image']
    )
    db.session.add(new_bag)
    db.session.commit()
    return jsonify({"message": "Bag created successfully!", "bag_id": new_bag.id}), 201


@app.route('/bags', methods=['GET'])
def get_bags():
    bags = bag.query.all()
    result = [
        {"id": b.id, "name": b.name, "price": b.price, "image": b.image}
        for b in bags
    ]
    return jsonify(result)


@app.route('/bags/<int:bag_id>', methods=['PUT'])
def update_bag(bag_id):
    data = request.get_json()
    bag_item = bag.query.get(bag_id)
    if not bag_item:
        return jsonify({"error": "Bag not found"}), 404

    bag_item.name = data.get('name', bag_item.name)
    bag_item.price = data.get('price', bag_item.price)
    bag_item.image = data.get('image', bag_item.image)
    db.session.commit()
    return jsonify({"message": "Bag updated successfully!"})


@app.route('/bags/<int:bag_id>', methods=['DELETE'])
def delete_bag(bag_id):
    bag_item = bag.query.get(bag_id)
    if not bag_item:
        return jsonify({"error": "Bag not found"}), 404

    db.session.delete(bag_item)
    db.session.commit()
    return jsonify({"message": "Bag deleted successfully!"})


# ----------------------- Caps -----------------------
@app.route('/caps', methods=['POST'])
def create_cap():
    data = request.get_json()
    new_cap = cap(
        name=data['name'],
        price=data['price'],
        image=data['image']
    )
    db.session.add(new_cap)
    db.session.commit()
    return jsonify({"message": "Cap created successfully!", "cap_id": new_cap.id}), 201


@app.route('/caps', methods=['GET'])
def get_caps():
    caps = cap.query.all()
    result = [
        {"id": c.id, "name": c.name, "price": c.price, "image": c.image}
        for c in caps
    ]
    return jsonify(result)


@app.route('/caps/<int:cap_id>', methods=['PUT'])
def update_cap(cap_id):
    data = request.get_json()
    cap_item = cap.query.get(cap_id)
    if not cap_item:
        return jsonify({"error": "Cap not found"}), 404

    cap_item.name = data.get('name', cap_item.name)
    cap_item.price = data.get('price', cap_item.price)
    cap_item.image = data.get('image', cap_item.image)
    db.session.commit()
    return jsonify({"message": "Cap updated successfully!"})


@app.route('/caps/<int:cap_id>', methods=['DELETE'])
def delete_cap(cap_id):
    cap_item = cap.query.get(cap_id)
    if not cap_item:
        return jsonify({"error": "Cap not found"}), 404

    db.session.delete(cap_item)
    db.session.commit()
    return jsonify({"message": "Cap deleted successfully!"})


# ----------------------- T-Shirts -----------------------
@app.route('/tshirts', methods=['POST'])
def create_tshirt():
    data = request.get_json()
    new_tshirt = tshirt(
        name=data['name'],
        price=data['price'],
        image=data['image']
    )
    db.session.add(new_tshirt)
    db.session.commit()
    return jsonify({"message": "T-Shirt created successfully!", "tshirt_id": new_tshirt.id}), 201


@app.route('/tshirts', methods=['GET'])
def get_tshirts():
    tshirts = tshirt.query.all()
    result = [
        {"id": t.id, "name": t.name, "price": t.price, "image": t.image}
        for t in tshirts
    ]
    return jsonify(result)


@app.route('/tshirts/<int:tshirt_id>', methods=['PUT'])
def update_tshirt(tshirt_id):
    data = request.get_json()
    tshirt_item = tshirt.query.get(tshirt_id)
    if not tshirt_item:
        return jsonify({"error": "T-Shirt not found"}), 404

    tshirt_item.name = data.get('name', tshirt_item.name)
    tshirt_item.price = data.get('price', tshirt_item.price)
    tshirt_item.image = data.get('image', tshirt_item.image)
    db.session.commit()
    return jsonify({"message": "T-Shirt updated successfully!"})


@app.route('/tshirts/<int:tshirt_id>', methods=['DELETE'])
def delete_tshirt(tshirt_id):
    tshirt_item = tshirt.query.get(tshirt_id)
    if not tshirt_item:
        return jsonify({"error": "T-Shirt not found"}), 404

    db.session.delete(tshirt_item)
    db.session.commit()
    return jsonify({"message": "T-Shirt deleted successfully!"})


if __name__ == '__main__':
    app.run(debug=True)
