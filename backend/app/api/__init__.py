"""
API Routes Module
"""

from flask import Blueprint

auth_bp = Blueprint("auth", __name__)
financial_bp = Blueprint("financial", __name__)
learning_bp = Blueprint("learning", __name__)

from . import auth  # noqa: E402, F401
from . import financial  # noqa: E402, F401
from . import learning  # noqa: E402, F401
