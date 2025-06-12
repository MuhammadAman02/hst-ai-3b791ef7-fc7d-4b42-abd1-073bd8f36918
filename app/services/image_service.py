import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
import os
import asyncio
from typing import Dict, Any, Tuple, Optional
from app.config import settings

class ImageService:
    """Service for image processing and manipulation operations."""
    
    def __init__(self):
        self.supported_formats = ['.jpg', '.jpeg', '.png', '.webp']
    
    async def load_image(self, file_path: str) -> np.ndarray:
        """Load and preprocess an image from file path."""
        try:
            # Validate file exists
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Image file not found: {file_path}")
            
            # Load image using OpenCV
            image = cv2.imread(file_path)
            if image is None:
                raise ValueError(f"Could not load image: {file_path}")
            
            # Convert BGR to RGB
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Resize if too large
            image = await self._resize_image(image)
            
            return image
            
        except Exception as e:
            raise Exception(f"Error loading image: {str(e)}")
    
    async def _resize_image(self, image: np.ndarray) -> np.ndarray:
        """Resize image if it exceeds maximum dimensions."""
        height, width = image.shape[:2]
        
        if width > settings.max_image_width or height > settings.max_image_height:
            # Calculate scaling factor
            scale_w = settings.max_image_width / width
            scale_h = settings.max_image_height / height
            scale = min(scale_w, scale_h)
            
            # Calculate new dimensions
            new_width = int(width * scale)
            new_height = int(height * scale)
            
            # Resize image
            image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
        
        return image
    
    async def adjust_skin_tone(self, image: np.ndarray, adjustments: Dict[str, Any]) -> np.ndarray:
        """Apply skin tone adjustments to an image."""
        try:
            # Convert to PIL Image for easier manipulation
            pil_image = Image.fromarray(image)
            
            # Apply brightness adjustment
            if adjustments.get('brightness', 0) != 0:
                brightness_factor = 1.0 + (adjustments['brightness'] / 100.0)
                enhancer = ImageEnhance.Brightness(pil_image)
                pil_image = enhancer.enhance(brightness_factor)
            
            # Apply saturation adjustment
            if adjustments.get('saturation', 0) != 0:
                saturation_factor = 1.0 + (adjustments['saturation'] / 100.0)
                enhancer = ImageEnhance.Color(pil_image)
                pil_image = enhancer.enhance(saturation_factor)
            
            # Convert back to numpy array for advanced adjustments
            adjusted_image = np.array(pil_image)
            
            # Apply warmth adjustment (color temperature)
            if adjustments.get('warmth', 0) != 0:
                adjusted_image = await self._adjust_color_temperature(
                    adjusted_image, adjustments['warmth']
                )
            
            # Apply hue shift
            if adjustments.get('hue_shift', 0) != 0:
                adjusted_image = await self._adjust_hue(
                    adjusted_image, adjustments['hue_shift']
                )
            
            return adjusted_image
            
        except Exception as e:
            raise Exception(f"Error adjusting skin tone: {str(e)}")
    
    async def _adjust_color_temperature(self, image: np.ndarray, warmth: int) -> np.ndarray:
        """Adjust the color temperature of an image."""
        # Convert to float for calculations
        image_float = image.astype(np.float32) / 255.0
        
        # Create temperature adjustment matrix
        if warmth > 0:  # Warmer (more red/yellow)
            factor = warmth / 50.0
            # Increase red and yellow channels
            image_float[:, :, 0] = np.clip(image_float[:, :, 0] * (1 + factor * 0.3), 0, 1)  # Red
            image_float[:, :, 1] = np.clip(image_float[:, :, 1] * (1 + factor * 0.2), 0, 1)  # Green
            image_float[:, :, 2] = np.clip(image_float[:, :, 2] * (1 - factor * 0.1), 0, 1)  # Blue
        else:  # Cooler (more blue)
            factor = abs(warmth) / 50.0
            # Increase blue channel, decrease red/yellow
            image_float[:, :, 0] = np.clip(image_float[:, :, 0] * (1 - factor * 0.2), 0, 1)  # Red
            image_float[:, :, 1] = np.clip(image_float[:, :, 1] * (1 - factor * 0.1), 0, 1)  # Green
            image_float[:, :, 2] = np.clip(image_float[:, :, 2] * (1 + factor * 0.3), 0, 1)  # Blue
        
        # Convert back to uint8
        return (image_float * 255).astype(np.uint8)
    
    async def _adjust_hue(self, image: np.ndarray, hue_shift: int) -> np.ndarray:
        """Adjust the hue of an image."""
        # Convert RGB to HSV
        hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
        
        # Adjust hue channel
        hue_adjustment = (hue_shift / 30.0) * 180  # Convert to OpenCV hue range
        hsv[:, :, 0] = (hsv[:, :, 0] + hue_adjustment) % 180
        
        # Convert back to RGB
        return cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)
    
    async def extract_face_region(self, image: np.ndarray) -> Optional[np.ndarray]:
        """Extract face region from image for more accurate skin tone analysis."""
        try:
            # Load face cascade classifier
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            
            # Convert to grayscale for face detection
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
            
            # Detect faces
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)
            
            if len(faces) > 0:
                # Use the largest face
                largest_face = max(faces, key=lambda x: x[2] * x[3])
                x, y, w, h = largest_face
                
                # Extract face region with some padding
                padding = int(min(w, h) * 0.1)
                x1 = max(0, x - padding)
                y1 = max(0, y - padding)
                x2 = min(image.shape[1], x + w + padding)
                y2 = min(image.shape[0], y + h + padding)
                
                face_region = image[y1:y2, x1:x2]
                return face_region
            
            return None
            
        except Exception as e:
            # If face detection fails, return None to use full image
            return None
    
    async def create_thumbnail(self, image: np.ndarray, size: int = None) -> np.ndarray:
        """Create a thumbnail version of the image."""
        if size is None:
            size = settings.thumbnail_size
        
        height, width = image.shape[:2]
        
        # Calculate scaling to maintain aspect ratio
        if width > height:
            new_width = size
            new_height = int(height * size / width)
        else:
            new_height = size
            new_width = int(width * size / height)
        
        # Resize image
        thumbnail = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
        return thumbnail
    
    async def save_processed_image(self, image: np.ndarray, filename: str) -> str:
        """Save processed image to uploads directory."""
        try:
            # Ensure filename has proper extension
            if not any(filename.lower().endswith(ext) for ext in self.supported_formats):
                filename += '.jpg'
            
            file_path = os.path.join(settings.upload_dir, filename)
            
            # Convert RGB to BGR for OpenCV saving
            bgr_image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            # Save image
            success = cv2.imwrite(file_path, bgr_image)
            
            if not success:
                raise Exception("Failed to save image")
            
            return file_path
            
        except Exception as e:
            raise Exception(f"Error saving processed image: {str(e)}")
    
    async def get_image_info(self, image: np.ndarray) -> Dict[str, Any]:
        """Get information about an image."""
        height, width, channels = image.shape
        
        return {
            'width': width,
            'height': height,
            'channels': channels,
            'size_bytes': image.nbytes,
            'dtype': str(image.dtype)
        }
    
    async def enhance_image_quality(self, image: np.ndarray) -> np.ndarray:
        """Apply basic image enhancement for better analysis."""
        try:
            # Convert to PIL for enhancement
            pil_image = Image.fromarray(image)
            
            # Slight sharpening
            enhancer = ImageEnhance.Sharpness(pil_image)
            pil_image = enhancer.enhance(1.1)
            
            # Slight contrast enhancement
            enhancer = ImageEnhance.Contrast(pil_image)
            pil_image = enhancer.enhance(1.05)
            
            return np.array(pil_image)
            
        except Exception as e:
            # Return original image if enhancement fails
            return image