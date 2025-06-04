from flask import request, abort, current_app

def require_admin():
    token = request.headers.get("Authorization")
    expected_token = f"Bearer {current_app.config['ADMIN_TOKEN']}"
    if token != expected_token:
        abort(403, description="Admin access required.")
