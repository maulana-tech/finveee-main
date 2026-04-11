"""
API Routes Module
"""

from flask import Blueprint

# Don't import routes here - they will be imported by app/__init__.py
# This just defines the blueprint names

__all__ = ["auth_bp", "financial_bp", "learning_bp"]
