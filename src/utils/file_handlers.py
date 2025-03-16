import sys
import os

# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import settings
import os

def get_media_path(file_path, direction='upload'):
    base_dir = settings.PATHS[f'media_{direction}']
    os.makedirs(base_dir, exist_ok=True)
    return os.path.abspath(os.path.join(base_dir, file_path))

def validate_file_path(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Path not found: {file_path}")
    if not os.path.isfile(file_path):
        raise IsADirectoryError(f"Expected file: {file_path}")
    return True
def validate_phone_number(number: str) -> bool:
    """Basic phone number validation"""
    return number.startswith('+') and number[1:].isdigit()
