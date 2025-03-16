import logging
from config import settings
import os

# Ensure the logs directory exists
os.makedirs(settings.PATHS['logs'], exist_ok=True)

logging.basicConfig(
    filename=os.path.join(settings.PATHS['logs'], 'whatsapp.log'),
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def handle_error(message, fatal=False):
    logging.error(message)
    print(f"⚠️ Error: {message}")
    if fatal:
        exit(1)
