"""
Application settings loaded from environment variables.
Values are read from a .env file in development; set directly in staging/production.
"""

import os

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL: str = os.environ["DATABASE_URL"]
APP_ENV: str = os.getenv("APP_ENV", "development")
