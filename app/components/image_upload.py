import os
import uuid
from typing import Callable, Optional
from nicegui import ui, events
from app.config import settings

class ImageUploadComponent:
    """Component for handling image uploads with drag-and-drop functionality."""
    
    def __init__(self, on_upload: Callable[[str, str], None]):
        self.on_upload = on_upload
        self.upload_area = None
        self.file_info = None
        self.create_component()
    
    def create_component(self):
        """Create the image upload UI component."""
        
        # Upload area container
        with ui.element('div').classes('w-full'):
            # File upload with drag and drop
            upload = ui.upload(
                on_upload=self._handle_upload,
                max_file_size=settings.max_file_size,
                multiple=False
            ).classes('w-full')
            
            # Custom upload area styling
            upload.props('accept="image/*"')
            upload.props('color="primary"')
            upload.props('flat')
            upload.props('bordered')
            
            # Upload area with custom styling
            with upload:
                with ui.element('div').classes('w-full p-8 text-center border-2 border-dashed border-gray-300 rounded-lg hover:border-primary transition-colors'):
                    ui.icon('cloud_upload').classes('text-6xl text-gray-400 mb-4')
                    ui.label('Drag and drop your photo here').classes('text-xl font-medium text-gray-600 mb-2')
                    ui.label('or click to browse').classes('text-gray-500')
                    ui.label('Supported formats: JPG, PNG, WebP (max 10MB)').classes('text-sm text-gray-400 mt-2')
            
            # File information display
            self.file_info = ui.element('div').classes('mt-4').style('display: none;')
            with self.file_info:
                with ui.row().classes('items-center gap-4 p-4 bg-gray-50 rounded-lg'):
                    ui.icon('image').classes('text-2xl text-primary')
                    self.file_name_label = ui.label('').classes('font-medium')
                    self.file_size_label = ui.label('').classes('text-sm text-gray-500')
                    ui.button('Remove', on_click=self._remove_file).props('flat color="negative" size="sm"')
    
    async def _handle_upload(self, e: events.UploadEventArguments):
        """Handle file upload event."""
        try:
            # Validate file type
            if not self._is_valid_file_type(e.name):
                ui.notify(f'❌ Invalid file type. Please upload an image file.', type='negative')
                return
            
            # Generate unique filename
            file_extension = os.path.splitext(e.name)[1].lower()
            unique_filename = f"{uuid.uuid4()}{file_extension}"
            file_path = os.path.join(settings.upload_dir, unique_filename)
            
            # Save uploaded file
            with open(file_path, 'wb') as f:
                f.write(e.content.read())
            
            # Update file info display
            self._update_file_info(e.name, len(e.content.read()))
            
            # Notify success
            ui.notify(f'✅ Image uploaded successfully: {e.name}', type='positive')
            
            # Call the upload callback
            await self.on_upload(file_path, e.name)
            
        except Exception as error:
            ui.notify(f'❌ Upload failed: {str(error)}', type='negative')
            print(f"Upload error: {error}")
    
    def _is_valid_file_type(self, filename: str) -> bool:
        """Check if the uploaded file has a valid extension."""
        file_extension = os.path.splitext(filename)[1].lower()
        return file_extension in settings.allowed_extensions
    
    def _update_file_info(self, filename: str, file_size: int):
        """Update the file information display."""
        self.file_name_label.text = filename
        self.file_size_label.text = f'{file_size / 1024 / 1024:.1f} MB'
        self.file_info.style('display: block;')
    
    def _remove_file(self):
        """Remove the uploaded file and reset the component."""
        self.file_info.style('display: none;')
        ui.notify('File removed', type='info')
    
    def reset(self):
        """Reset the upload component."""
        self.file_info.style('display: none;')