import os
from dotenv import load_dotenv

load_dotenv()

# Database Configuration
DB_NAME = "users.db"

# Admin Configuration
ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')
SECRET_KEY = os.getenv('SECRET_KEY', os.urandom(24).hex())

# Session Configuration
SESSION_TIMEOUT_MINUTES = int(os.getenv('SESSION_TIMEOUT_MINUTES', '30'))

# Logging Configuration
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = os.getenv('LOG_FILE', 'app.log')