"""
Finvee Backend - Auth API Routes
"""

from flask import request, jsonify
import traceback

from . import auth_bp


@auth_bp.route("/register", methods=["POST"])
def register():
    """Register a new user"""
    try:
        data = request.get_json()

        from ..models.user import UserManager

        um = UserManager()

        # Check if email exists
        existing = um.get_user_by_email(data.get("email"))
        if existing:
            return jsonify({"success": False, "error": "Email already registered"}), 400

        user = um.create_user(
            email=data.get("email"),
            username=data.get("username"),
            password=data.get("password"),
            full_name=data.get("full_name"),
        )

        return jsonify({"success": True, "data": user.to_dict()})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@auth_bp.route("/login", methods=["POST"])
def login():
    """Login user"""
    try:
        data = request.get_json()

        from ..models.user import UserManager

        um = UserManager()

        user = um.verify_password(data.get("email"), data.get("password"))

        if not user:
            return jsonify({"success": False, "error": "Invalid credentials"}), 401

        # Create session
        import uuid
        import hashlib
        from datetime import datetime, timedelta

        token = hashlib.sha256(
            f"{user.user_id}{datetime.now().isoformat()}".encode()
        ).hexdigest()
        expires = (datetime.now() + timedelta(days=7)).isoformat()

        session_data = {
            "session_id": f"sess_{uuid.uuid4().hex[:12]}",
            "user_id": user.user_id,
            "token": token,
            "created_at": datetime.now().isoformat(),
            "expires_at": expires,
            "is_active": True,
        }

        return jsonify(
            {
                "success": True,
                "data": {"user": user.to_dict(), "token": token, "expires_at": expires},
            }
        )
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@auth_bp.route("/me", methods=["GET"])
def get_current_user():
    """Get current user info"""
    try:
        user_id = request.headers.get("X-User-ID")
        if not user_id:
            return jsonify({"success": False, "error": "Authentication required"}), 401

        from ..models.user import UserManager

        um = UserManager()

        user = um.get_user(user_id)

        if not user:
            return jsonify({"success": False, "error": "User not found"}), 404

        return jsonify({"success": True, "data": user.to_dict()})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@auth_bp.route("/logout", methods=["POST"])
def logout():
    """Logout user"""
    return jsonify({"success": True, "message": "Logged out"})
