"""
Finvee Configuration
Load from project root .env file
"""

import os
from dotenv import load_dotenv

project_root_env = os.path.join(os.path.dirname(__file__), "../../.env")

if os.path.exists(project_root_env):
    load_dotenv(project_root_env, override=True)
else:
    load_dotenv(override=True)


class Config:
    """Flask Configuration"""

    SECRET_KEY = os.environ.get("SECRET_KEY", "finvee-secret-key")
    DEBUG = os.environ.get("FLASK_DEBUG", "True").lower() == "true"

    JSON_AS_ASCII = False

    # LLM Configuration (optional for Finvee)
    LLM_API_KEY = os.environ.get("LLM_API_KEY")
    LLM_BASE_URL = os.environ.get("LLM_BASE_URL", "https://api.openai.com/v1")
    LLM_MODEL_NAME = os.environ.get("LLM_MODEL_NAME", "gpt-4o-mini")

    # File upload config
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "../uploads")
    ALLOWED_EXTENSIONS = {"pdf", "md", "txt", "csv", "xlsx", "xls"}

    # Data directory
    DATA_DIR = os.path.join(os.path.dirname(__file__), "../data")

    @classmethod
    def validate(cls):
        """Validate required config - LLM is optional for Finvee"""
        errors = []
        # LLM is optional for basic features
        return errors
