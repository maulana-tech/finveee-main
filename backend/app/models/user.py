"""
Finvee Backend - Core Models
User, Authentication, and Base Models
"""

from datetime import datetime
from typing import Optional, List
from dataclasses import dataclass, field
import uuid
import json


def generate_id(prefix: str = "") -> str:
    return f"{prefix}{uuid.uuid4().hex[:12]}"


@dataclass
class User:
    user_id: str
    email: str
    username: str
    password_hash: str
    full_name: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    is_active: bool = True
    role: str = "user"  # user, admin

    def __post_init__(self):
        # Ensure required fields are set
        if not self.user_id:
            raise ValueError("user_id is required")
        if not self.email:
            raise ValueError("email is required")
        if not self.username:
            raise ValueError("username is required")
        if not self.password_hash:
            raise ValueError("password_hash is required")

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "email": self.email,
            "username": self.username,
            "password_hash": self.password_hash,
            "full_name": self.full_name,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "is_active": self.is_active,
            "role": self.role,
        }


@dataclass
class Session:
    session_id: str
    user_id: str
    token: str
    expires_at: str
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    is_active: bool = True

    def to_dict(self):
        return {
            "session_id": self.session_id,
            "user_id": self.user_id,
            "token": self.token,
            "created_at": self.created_at,
            "expires_at": self.expires_at,
            "is_active": self.is_active,
        }


class UserManager:
    _instance = None
    _users: dict = {}
    _sessions: dict = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._load_users()
        return cls._instance

    @classmethod
    def _load_users(cls):
        import os

        users_file = os.path.join(os.path.dirname(__file__), "../../data/users.json")
        if os.path.exists(users_file):
            with open(users_file, "r") as f:
                data = json.load(f)
                cls._users = {u["user_id"]: u for u in data.get("users", [])}

    def create_user(
        self, email: str, username: str, password: str, full_name: str = None
    ) -> User:
        import hashlib

        user_id = generate_id("user_")
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        user = User(
            user_id=user_id,
            email=email,
            username=username,
            password_hash=password_hash,
            full_name=full_name,
        )

        self._users[user_id] = user.to_dict()
        self._save_users()
        return user

    def verify_password(self, email: str, password: str) -> Optional[User]:
        import hashlib

        password_hash = hashlib.sha256(password.encode()).hexdigest()

        for user_data in self._users.values():
            if (
                user_data["email"] == email
                and user_data["password_hash"] == password_hash
            ):
                return User(**user_data)
        return None

    def get_user(self, user_id: str) -> Optional[User]:
        user_data = self._users.get(user_id)
        if user_data:
            return User(**user_data)
        return None

    def get_user_by_email(self, email: str) -> Optional[User]:
        for user_data in self._users.values():
            if user_data["email"] == email:
                return User(**user_data)
        return None

    def _save_users(self):
        import os

        data_dir = os.path.join(os.path.dirname(__file__), "../../data")
        os.makedirs(data_dir, exist_ok=True)
        users_file = os.path.join(data_dir, "users.json")

        with open(users_file, "w") as f:
            json.dump({"users": list(self._users.values())}, f, indent=2)
