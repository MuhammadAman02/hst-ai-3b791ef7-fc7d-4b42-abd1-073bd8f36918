import os
from typing import List, Optional
from pydantic import Field, validator
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application configuration settings."""
    
    # Application settings
    app_name: str = Field(default="Color Harmony - AI Skin Tone Analysis", description="Application name")
    debug: bool = Field(default=False, description="Debug mode")
    
    # Server settings
    host: str = Field(default="0.0.0.0", description="Server host")
    port: int = Field(default=8000, description="Server port")
    
    # File upload settings
    upload_dir: str = Field(default="uploads", description="Upload directory")
    max_file_size: int = Field(default=10 * 1024 * 1024, description="Maximum file size in bytes (10MB)")
    allowed_extensions: List[str] = Field(default=[".jpg", ".jpeg", ".png", ".webp"], description="Allowed file extensions")
    
    # Image processing settings
    max_image_width: int = Field(default=1920, description="Maximum image width")
    max_image_height: int = Field(default=1080, description="Maximum image height")
    thumbnail_size: int = Field(default=300, description="Thumbnail size")
    
    # Analysis settings
    confidence_threshold: float = Field(default=0.7, description="Minimum confidence for analysis")
    max_colors_extract: int = Field(default=5, description="Maximum colors to extract")
    
    # Security settings
    cors_origins: List[str] = Field(default=["*"], description="CORS allowed origins")
    
    @validator('allowed_extensions', pre=True)
    def parse_allowed_extensions(cls, v):
        """Parse allowed extensions from string or list."""
        if isinstance(v, str):
            # Handle comma-separated string from environment
            return [ext.strip() for ext in v.split(',') if ext.strip()]
        elif isinstance(v, list):
            return v
        else:
            return [".jpg", ".jpeg", ".png", ".webp"]
    
    @validator('cors_origins', pre=True)
    def parse_cors_origins(cls, v):
        """Parse CORS origins from string or list."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(',') if origin.strip()]
        elif isinstance(v, list):
            return v
        else:
            return ["*"]
    
    def __init__(self, **kwargs):
        """Initialize settings and create upload directory."""
        super().__init__(**kwargs)
        
        # Create upload directory if it doesn't exist
        if not os.path.exists(self.upload_dir):
            os.makedirs(self.upload_dir, exist_ok=True)
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

# Create settings instance with error handling
try:
    settings = Settings()
except Exception as e:
    print(f"Warning: Error loading settings from .env file: {e}")
    print("Using default settings...")
    settings = Settings(_env_file=None)  # Skip .env file loading