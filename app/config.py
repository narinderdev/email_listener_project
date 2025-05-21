import os
from dotenv import load_dotenv

load_dotenv()  # Loads variables from .env

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
KEYWORD = os.getenv("KEYWORD")
DB_URL = os.getenv("DB_URL")
ENDPOINT_URL = os.getenv("ENDPOINT_URL")
POLL_INTERVAL = int(os.getenv("POLL_INTERVAL", 60))
