import os
import uuid
import hashlib
from typing import Any, Dict, List, Optional
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_unique_filename(original_filename: str) -> str:
    """Generate a unique filename while preserving the extension."""
    name, ext = os.path.splitext(original_filename)
    unique_id = str(uuid.uuid4())
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{timestamp}_{unique_id}{ext}"

def validate_image_file(filename: str, allowed_extensions: List[str]) -> bool:
    """Validate if a file is an allowed image type."""
    if not filename:
        return False
    
    extension = os.path.splitext(filename)[1].lower().lstrip('.')
    return extension in [ext.lower() for ext in allowed_extensions]

def calculate_file_hash(file_path: str) -> str:
    """Calculate SHA-256 hash of a file."""
    hash_sha256 = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()
    except Exception as e:
        logger.error(f"Error calculating file hash: {e}")
        return ""

def safe_filename(filename: str) -> str:
    """Create a safe filename by removing/replacing unsafe characters."""
    import re
    # Remove or replace unsafe characters
    safe_name = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Remove leading/trailing spaces and dots
    safe_name = safe_name.strip(' .')
    # Limit length
    if len(safe_name) > 255:
        name, ext = os.path.splitext(safe_name)
        safe_name = name[:255-len(ext)] + ext
    
    return safe_name or "unnamed_file"

def format_file_size(size_bytes: int) -> str:
    """Format file size in human-readable format."""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    import math
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_names[i]}"

def cleanup_old_files(directory: str, max_age_hours: int = 24) -> int:
    """Clean up old files in a directory."""
    if not os.path.exists(directory):
        return 0
    
    current_time = datetime.now()
    deleted_count = 0
    
    try:
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path):
                file_time = datetime.fromtimestamp(os.path.getctime(file_path))
                age_hours = (current_time - file_time).total_seconds() / 3600
                
                if age_hours > max_age_hours:
                    os.remove(file_path)
                    deleted_count += 1
                    logger.info(f"Deleted old file: {filename}")
    
    except Exception as e:
        logger.error(f"Error during file cleanup: {e}")
    
    return deleted_count

def validate_color_hex(hex_color: str) -> bool:
    """Validate if a string is a valid hex color code."""
    import re
    pattern = r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$'
    return bool(re.match(pattern, hex_color))

def rgb_to_hex(r: int, g: int, b: int) -> str:
    """Convert RGB values to hex color code."""
    return f"#{r:02x}{g:02x}{b:02x}"

def hex_to_rgb(hex_color: str) -> tuple:
    """Convert hex color code to RGB values."""
    hex_color = hex_color.lstrip('#')
    if len(hex_color) == 3:
        hex_color = ''.join([c*2 for c in hex_color])
    
    try:
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    except ValueError:
        return (0, 0, 0)

def create_error_response(message: str, error_type: str = "general", details: Any = None) -> Dict[str, Any]:
    """Create a standardized error response."""
    return {
        "error": True,
        "message": message,
        "error_type": error_type,
        "details": details,
        "timestamp": datetime.now().isoformat()
    }

def create_success_response(data: Any = None, message: str = "Success") -> Dict[str, Any]:
    """Create a standardized success response."""
    return {
        "error": False,
        "message": message,
        "data": data,
        "timestamp": datetime.now().isoformat()
    }

class ColorAnalysisError(Exception):
    """Custom exception for color analysis errors."""
    pass

class ImageProcessingError(Exception):
    """Custom exception for image processing errors."""
    pass

class FileUploadError(Exception):
    """Custom exception for file upload errors."""
    pass