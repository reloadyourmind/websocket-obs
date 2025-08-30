import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# OBS WebSocket Configuration
OBS_HOST = os.getenv('OBS_HOST', 'localhost')
OBS_PORT = int(os.getenv('OBS_PORT', 4455))
OBS_PASSWORD = os.getenv('OBS_PASSWORD', '')

# Remote Server Configuration
SERVER_HOST = os.getenv('SERVER_HOST', '0.0.0.0')
SERVER_PORT = int(os.getenv('SERVER_PORT', 5000))
SERVER_DEBUG = os.getenv('SERVER_DEBUG', 'True').lower() == 'true'

# Network Configuration
ALLOWED_ORIGINS = os.getenv('ALLOWED_ORIGINS', '*').split(',')

# Logging Configuration
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'