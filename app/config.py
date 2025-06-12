from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    """Application configuration settings."""
    
    port: int = 8000
    host: str = "0.0.0.0"
    debug: bool = False
    
    # File upload settings
    upload_dir: str = "static/uploads"
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    allowed_extensions: List[str] = ["jpg", "jpeg", "png", "webp"]
    
    # Image processing settings
    max_image_width: int = 1024
    max_image_height: int = 1024
    thumbnail_size: int = 300
    
    # Color analysis settings
    skin_tone_clusters: int = 5
    color_palette_size: int = 12
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Global settings instance
settings = Settings()

# Ensure upload directory exists
os.makedirs(settings.upload_dir, exist_ok=True)