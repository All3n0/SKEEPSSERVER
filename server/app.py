import datetime
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
@app.route('/custom-orders', methods=['GET'])
def get_custom_orders():
    orders = CustomOrder.query.order_by(CustomOrder.created_at.desc()).all()
    return jsonify([order.to_dict() for order in orders])

@app.route('/custom-orders/<int:order_id>', methods=['DELETE'])
def delete_custom_order(order_id):
    order = CustomOrder.query.get_or_404(order_id)
    db.session.delete(order)
    db.session.commit()
    return jsonify({'message': 'Custom order deleted successfully'})

@app.route('/custom-orders/stats', methods=['GET'])
def custom_orders_stats():
    total = CustomOrder.query.count()
    recent = CustomOrder.query.filter(
        CustomOrder.created_at >= datetime.datetime.now() - datetime.timedelta(days=7)
    ).count()
    
    return jsonify({
        'total': total,
        'recent': recent
    })
import json
import os
from datetime import datetime
from flask import request, jsonify
from auth.admin_auth import require_admin

# Backup route - exports all data to JSON
@app.route('/api/admin/export', methods=['POST'])

def export_database():
    """Export all database data to JSON backup file"""
    try:
        # Collect data from all tables
        backup_data = {
            'timestamp': datetime.now().isoformat(),
            'bags': [bag.to_dict() for bag in Bag.query.all()],
            'tshirts': [tshirt.to_dict() for tshirt in Tshirt.query.all()],
            'hoodies': [{
                'id': hoodie.id,
                'name': hoodie.name,
                'inspiration': hoodie.inspiration,
                'price': hoodie.price,
                'image': hoodie.image
            } for hoodie in Hoodie.query.all()],
            'orders': [order.to_dict() for order in Order.query.all()],
            'custom_orders': [co.to_dict() for co in CustomOrder.query.all()]
        }
        
        # Create backup filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_filename = f'database_backup_{timestamp}.json'
        
        # Save to file (in Railway persistent storage if available)
        if os.environ.get('RAILWAY_VOLUME_MOUNT_PATH'):
            backup_dir = os.path.join(os.environ.get('RAILWAY_VOLUME_MOUNT_PATH'), 'backups')
        else:
            backup_dir = 'backups'
        
        os.makedirs(backup_dir, exist_ok=True)
        backup_path = os.path.join(backup_dir, backup_filename)
        
        with open(backup_path, 'w') as f:
            json.dump(backup_data, f, indent=2)
        
        # Also create a "latest" copy for auto-restore
        latest_backup = os.path.join(backup_dir, 'latest_backup.json')
        with open(latest_backup, 'w') as f:
            json.dump(backup_data, f, indent=2)
        
        return jsonify({
            'success': True,
            'message': f'Database exported successfully. {len(backup_data["bags"])} bags, {len(backup_data["tshirts"])} tshirts, {len(backup_data["hoodies"])} hoodies, {len(backup_data["orders"])} orders, {len(backup_data["custom_orders"])} custom orders backed up.',
            'backup_file': backup_path,
            'stats': {
                'bags': len(backup_data['bags']),
                'tshirts': len(backup_data['tshirts']),
                'hoodies': len(backup_data['hoodies']),
                'orders': len(backup_data['orders']),
                'custom_orders': len(backup_data['custom_orders'])
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Restore route - imports data from JSON backup
@app.route('/api/admin/import', methods=['POST'])

def import_database():
    """Import database data from JSON backup file"""
    try:
        data = request.get_json()
        
        # Allow specifying a backup file, otherwise use latest
        backup_dir = None
        if os.environ.get('RAILWAY_VOLUME_MOUNT_PATH'):
            backup_dir = os.path.join(os.environ.get('RAILWAY_VOLUME_MOUNT_PATH'), 'backups')
        else:
            backup_dir = 'backups'
        
        backup_path = None
        if data and data.get('backup_file'):
            # Use specified backup file
            backup_path = data.get('backup_file')
        else:
            # Use latest backup
            latest_backup = os.path.join(backup_dir, 'latest_backup.json')
            if os.path.exists(latest_backup):
                backup_path = latest_backup
            else:
                # Find most recent backup
                backup_files = [f for f in os.listdir(backup_dir) if f.startswith('database_backup_') and f.endswith('.json')]
                if backup_files:
                    backup_files.sort(reverse=True)
                    backup_path = os.path.join(backup_dir, backup_files[0])
        
        if not backup_path or not os.path.exists(backup_path):
            return jsonify({
                'success': False,
                'error': 'No backup file found. Please create a backup first or specify a backup file.'
            }), 404
        
        # Read backup file
        with open(backup_path, 'r') as f:
            backup_data = json.load(f)
        
        # Clear existing data (optional - you might want to skip this)
        clear_existing = data.get('clear_existing', True) if data else True
        
        if clear_existing:
            print("Clearing existing data...")
            # Delete all data while preserving tables
            OrderItem.query.delete()
            Order.query.delete()
            CustomOrder.query.delete()
            Bag.query.delete()
            Tshirt.query.delete()
            Hoodie.query.delete()
            db.session.commit()
        
        # Restore Bags
        bags_restored = 0
        for bag_data in backup_data.get('bags', []):
            # Check if bag already exists
            existing_bag = Bag.query.filter_by(
                name=bag_data['name'],
                inspiration=bag_data.get('inspiration', '')
            ).first()
            
            if not existing_bag:
                new_bag = Bag(
                    name=bag_data['name'],
                    price=bag_data['price'],
                    image=bag_data['image'],
                    inspiration=bag_data.get('inspiration', '')
                )
                db.session.add(new_bag)
                bags_restored += 1
        
        # Restore Tshirts
        tshirts_restored = 0
        for tshirt_data in backup_data.get('tshirts', []):
            existing_tshirt = Tshirt.query.filter_by(
                name=tshirt_data['name'],
                inspiration=tshirt_data.get('inspiration', '')
            ).first()
            
            if not existing_tshirt:
                new_tshirt = Tshirt(
                    name=tshirt_data['name'],
                    price=tshirt_data['price'],
                    image=tshirt_data['image'],
                    inspiration=tshirt_data.get('inspiration', '')
                )
                db.session.add(new_tshirt)
                tshirts_restored += 1
        
        # Restore Hoodies
        hoodies_restored = 0
        for hoodie_data in backup_data.get('hoodies', []):
            existing_hoodie = Hoodie.query.filter_by(
                name=hoodie_data['name'],
                inspiration=hoodie_data.get('inspiration', '')
            ).first()
            
            if not existing_hoodie:
                new_hoodie = Hoodie(
                    name=hoodie_data['name'],
                    price=hoodie_data['price'],
                    image=hoodie_data['image'],
                    inspiration=hoodie_data.get('inspiration', '')
                )
                db.session.add(new_hoodie)
                hoodies_restored += 1
        
        # Restore Orders (with their items)
        orders_restored = 0
        for order_data in backup_data.get('orders', []):
            # Check if order already exists
            existing_order = Order.query.filter_by(
                customer_email=order_data['customer_email'],
                customer_name=order_data['customer_name']
            ).first()
            
            if not existing_order:
                new_order = Order(
                    customer_name=order_data['customer_name'],
                    customer_email=order_data['customer_email'],
                    instagram_handle=order_data.get('instagram_handle'),
                    completed=order_data.get('completed', False)
                )
                db.session.add(new_order)
                db.session.flush()  # Get the ID
                
                # Add order items
                for item_data in order_data.get('items', []):
                    order_item = OrderItem(
                        order_id=new_order.id,
                        product_type=item_data['product_type'],
                        product_name=item_data.get('product_name', ''),
                        quantity=item_data['quantity'],
                        price=item_data['price']
                    )
                    db.session.add(order_item)
                
                orders_restored += 1
        
        # Restore Custom Orders
        custom_orders_restored = 0
        for co_data in backup_data.get('custom_orders', []):
            existing_co = CustomOrder.query.filter_by(
                email=co_data['email'],
                name=co_data['name'],
                created_at=datetime.fromisoformat(co_data['created_at'].replace('Z', '+00:00'))
            ).first()
            
            if not existing_co:
                new_co = CustomOrder(
                    name=co_data['name'],
                    email=co_data['email'],
                    phone=co_data.get('phone'),
                    project_type=co_data['project_type'],
                    message=co_data['message'],
                    created_at=datetime.fromisoformat(co_data['created_at'].replace('Z', '+00:00'))
                )
                db.session.add(new_co)
                custom_orders_restored += 1
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Database restored successfully from {backup_path}',
            'backup_timestamp': backup_data.get('timestamp'),
            'restored_counts': {
                'bags': bags_restored,
                'tshirts': tshirts_restored,
                'hoodies': hoodies_restored,
                'orders': orders_restored,
                'custom_orders': custom_orders_restored
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Auto-backup and restore script for Railway redeploys
@app.route('/api/admin/migrate-data', methods=['POST'])

def migrate_data():
    """
    One-click solution for Railway redeploys:
    1. Export current data to persistent storage
    2. Can be called right before redeploy
    """
    try:
        # Step 1: Export current data
        export_response = export_database()
        
        # Parse the response
        if export_response[0].json['success']:
            backup_file = export_response[0].json['backup_file']
            
            # Step 2: Return instructions for restore
            return jsonify({
                'success': True,
                'message': 'Data migration ready for redeploy',
                'backup_file': backup_file,
                'instructions': {
                    '1': 'Run this export before redeploying on Railway',
                    '2': 'After redeploy completes, call /api/admin/import',
                    '3': 'Or use this curl command to restore:',
                    'curl': f'curl -X POST {request.host_url}api/admin/import -H "Authorization: Bearer {app.config["ADMIN_TOKEN"]}"'
                }
            }), 200
        else:
            return export_response
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
@app.route('/api/admin/backups', methods=['GET'])

def list_backups():
    """List all available backup files"""
    try:
        if os.environ.get('RAILWAY_VOLUME_MOUNT_PATH'):
            backup_dir = os.path.join(os.environ.get('RAILWAY_VOLUME_MOUNT_PATH'), 'backups')
        else:
            backup_dir = 'backups'
        
        backups = []
        if os.path.exists(backup_dir):
            for filename in os.listdir(backup_dir):
                if filename.endswith('.json'):
                    filepath = os.path.join(backup_dir, filename)
                    stat = os.stat(filepath)
                    backups.append({
                        'filename': filename,
                        'path': filepath,
                        'size': stat.st_size,
                        'created': datetime.fromtimestamp(stat.st_ctime).isoformat(),
                        'modified': datetime.fromtimestamp(stat.st_mtime).isoformat()
                    })
        
        # Sort by created date (newest first)
        backups.sort(key=lambda x: x['created'], reverse=True)
        
        return jsonify({
            'success': True,
            'backups': backups,
            'backup_dir': backup_dir,
            'total_backups': len(backups)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
if __name__ == '__main__':
    app.run(debug=True)