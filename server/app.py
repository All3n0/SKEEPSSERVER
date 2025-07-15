from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from flask_mail import Mail, Message
from config import create_app, db
from models import CustomOrder, Order, OrderItem, Bag,Hoodie, Tshirt
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


# ----------------------- General Routes -----------------------
@app.route('/')
def index():
    return "Yee,skeeps!"


# ----------------------- Search Route -----------------------
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


# ----------------------- Order Routes -----------------------
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
            quantity=item.get("quantity", 1),
            price=float(item.get("price", 0))
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

            Thank you for placing an order with Skeeps Collection! We're thrilled to prepare your items and get them to you as soon as possible. Here's a quick summary of your order:

            Instagram Handle: @{instagram_handle or 'N/A'}  
            Items Ordered:  
            {chr(10).join(item_descriptions)}  
            Total Amount: Ksh {total_price}

            We will be reaching out shortly through instagram with payment details and next steps. If you have any questions or would like to make adjustments to your order, feel free to reach out through our Instagram or reply directly to this message.

            Warm regards,  
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
                    "quantity": item.quantity,
                    "price": item.price
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


# ----------------------- Bag Routes -----------------------
@app.route('/bags', methods=['POST'])
def create_bag():
    
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
            "image": b.image,
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

@app.route('/all_bags', methods=['GET'])
def get_all_bags():
    bags = Bag.query.all()
    return jsonify([bag.to_dict() for bag in bags]), 200


# ----------------------- Hoodie Routes -----------------------
@app.route('/hoodies', methods=['GET'])
def get_hoodie_inspirations():
    inspirations = (
        Hoodie.query.distinct(Hoodie.inspiration)
        .group_by(Hoodie.inspiration)
        .all()
    )
    result = [
        {
            "inspiration": h.inspiration,
            "image": h.image,
            "name": h.name,
            "price": float(h.price) if h.price else 0.00
        }
        for h in inspirations
    ]
    return jsonify(result)

@app.route('/hoodies/inspiration/<string:inspiration>', methods=['GET'])
def get_hoodies_by_inspiration(inspiration):
    hoodies = Hoodie.query.filter_by(inspiration=inspiration).all()
    result = [
        {
            "id": h.id,
            "name": h.name,
            "price": float(h.price) if h.price else 0.00,
            "image": h.image,
        }
        for h in hoodies
    ]
    return jsonify(result)

@app.route('/hoodies', methods=['POST'])
def create_hoodie():
    
    data = request.get_json()
    new_hoodie = Hoodie(
        name=data['name'],
        price=data['price'],
        image=data['image'],
        inspiration=data.get('inspiration', '')
    )
    db.session.add(new_hoodie)
    db.session.commit()
    return jsonify({"message": "Hoodie created successfully!", "hoodie_id": new_hoodie.id}), 201

# GET ALL HOODIES
@app.route('/all_hoodies', methods=['GET'])
def get_all_hoodies():
    hoodies = Hoodie.query.all()
    return jsonify([{
        'id': h.id,
        'name': h.name,
        'price': h.price,
        'image': h.image,
        'inspiration': h.inspiration
    } for h in hoodies]), 200

# UPDATE HOODIE
@app.route('/hoodies/<int:hoodie_id>', methods=['PUT'])
def update_hoodie(hoodie_id):
    data = request.get_json()
    hoodie = Hoodie.query.get(hoodie_id)
    if not hoodie:
        return jsonify({"error": "Hoodie not found"}), 404
    hoodie.name = data.get('name', hoodie.name)
    hoodie.price = data.get('price', hoodie.price)
    hoodie.image = data.get('image', hoodie.image)
    hoodie.inspiration = data.get('inspiration', hoodie.inspiration)
    db.session.commit()
    return jsonify({"message": "Hoodie updated successfully!"})

# DELETE HOODIE
@app.route('/hoodies/<int:hoodie_id>', methods=['DELETE'])
def delete_hoodie(hoodie_id):
    hoodie = Hoodie.query.get(hoodie_id)
    if not hoodie:
        return jsonify({"error": "Hoodie not found"}), 404
    db.session.delete(hoodie)
    db.session.commit()
    return jsonify({"message": "Hoodie deleted successfully!"})
# ----------------------- T-Shirt Routes -----------------------
@app.route('/tshirts', methods=['POST'])
def create_tshirt():
    
    data = request.get_json()
    new_tshirt = Tshirt(
        name=data['name'],
        inspiration=data['inspiration'],
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
            "image": t.image,
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

@app.route('/all_tshirts', methods=['GET'])
def get_all_tshirts():
    tshirts = Tshirt.query.all()
    return jsonify([tshirt.to_dict() for tshirt in tshirts]), 200
@app.route('/dashboard/stats')
def dashboard_stats():
    total_products = Bag.query.count() + Tshirt.query.count() + Hoodie.query.count()
    total_orders = Order.query.count()
    total_customers = db.session.query(Order.customer_email).distinct().count()
    revenue = db.session.query(db.func.sum(OrderItem.price * OrderItem.quantity)).scalar() or 0

    return jsonify({
        "total_products": total_products,
        "total_orders": total_orders,
        "total_customers": total_customers,
        "revenue": round(revenue, 2)
    })
@app.route('/dashboard/recent-orders')
def dashboard_recent_orders():
    try:
        orders = Order.query.order_by(Order.id.desc()).limit(4).all()
        recent = []
        for o in orders:
            order_items = []
            total_amount = 0
            for item in o.items:
                order_items.append({
                    "product_name": item.product_name,
                    "quantity": item.quantity,
                    "price": item.price
                })
                total_amount += item.price * item.quantity
            
            # Create the order dictionary with fallback values
            order_data = {
                "id": f"ORD{o.id:03}",
                "customer_name": o.customer_name or "Unknown",
                "customer_email": o.customer_email or "",
                "products": [item.product_name for item in o.items],
                "status": "completed" if o.completed else "pending",
                "amount": f"Ksh {total_amount:.2f}",
                "items": order_items,
                "created_at": None,  # Default value since we don't have this field
                "completed": o.completed if hasattr(o, 'completed') else False
            }
            recent.append(order_data)
        return jsonify(recent)
    except Exception as e:
        app.logger.error(f"Error in dashboard_recent_orders: {str(e)}")
        return jsonify({"error": "Failed to fetch recent orders"}), 500

@app.route("/contact", methods=["POST", "OPTIONS"])
def handle_contact_form():
    if request.method == "OPTIONS":
        # Handle preflight request
        response = jsonify({"message": "Preflight request accepted"})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "*")
        response.headers.add("Access-Control-Allow-Methods", "*")
        return response

    data = request.get_json()

    # Validate required fields
    required_fields = ['name', 'email', 'project', 'message']
    for field in required_fields:
        if not data.get(field):
            return jsonify({"error": f"Missing required field: {field}"}), 400

    try:
        # Save to custom_orders table
        custom_order = CustomOrder(
            name=data['name'],
            email=data['email'],
            phone=data.get('phone', ''),
            project_type=data['project'],
            message=data['message']
        )
        db.session.add(custom_order)
        db.session.commit()

        # Send confirmation email
        try:
            msg = Message("Skeeps Collection Quote Request Received",
                          sender='skeepscollection@gmail.com',
                          recipients=[data['email']])
            msg.body = f"""
Hello {data['name']},

Thank you for reaching out to Skeeps Collection! We've received your request for a custom {data['project'].lower()} and will get back to you within 24 hours.

Your message:
--------------------
{data['message']}
--------------------

Phone: {data.get('phone', 'N/A')}

We'll contact you soon with a quote and any further questions.

Best regards,  
Skeeps Collection Team
            """
            mail.send(msg)
        except Exception as e:
            print("Failed to send contact email:", e)

        response = jsonify({
            "message": "Thank you for your submission! We will get back to you soon.",
            "submission_id": custom_order.id
        })
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response, 201

    except Exception as e:
        db.session.rollback()
        response = jsonify({"error": str(e)})
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response, 500

if __name__ == '__main__':
    app.run(debug=True)