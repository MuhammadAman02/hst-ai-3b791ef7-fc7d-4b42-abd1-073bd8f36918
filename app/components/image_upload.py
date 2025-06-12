from nicegui import ui, events
from typing import Callable, Optional
import os
import uuid
from app.config import settings

class ImageUploadComponent:
    """Component for handling image uploads with drag-and-drop support."""
    
    def __init__(self, on_upload: Callable[[str], None], max_size: int = 10*1024*1024):
        self.on_upload = on_upload
        self.max_size = max_size
        self.upload_area = None
        self.file_info = None
        self.create_component()
    
    def create_component(self):
        """Create the image upload UI component."""
        with ui.column().classes('w-full gap-4'):
            # Upload area
            with ui.card().classes('w-full p-8 border-2 border-dashed border-gray-300 hover:border-blue-400 transition-colors cursor-pointer'):
                with ui.column().classes('items-center gap-4'):
                    ui.icon('cloud_upload', size='3rem').classes('text-gray-400')
                    ui.label('Drag & drop your photo here').classes('text-lg font-medium text-gray-600')
                    ui.label('or click to browse').classes('text-sm text-gray-500')
                    ui.label(f'Max file size: {self.max_size // (1024*1024)}MB').classes('text-xs text-gray-400')
                    
                    # Hidden file input
                    self.file_input = ui.upload(
                        on_upload=self._handle_upload,
                        max_file_size=self.max_size,
                        max_files=1
                    ).classes('hidden').props('accept="image/*"')
            
            # File info display
            self.file_info = ui.row().classes('w-full items-center gap-2').style('display: none;')
            with self.file_info:
                ui.icon('image', size='sm').classes('text-green-500')
                self.file_name_label = ui.label('').classes('text-sm font-medium')
                self.file_size_label = ui.label('').classes('text-xs text-gray-500')
    
    async def _handle_upload(self, e: events.UploadEventArguments):
        """Handle the file upload event."""
        try:
            # Validate file type
            if not self._is_valid_image(e.name):
                ui.notify('Please upload a valid image file (JPG, PNG, WebP)', type='negative')
                return
            
            # Generate unique filename
            file_extension = os.path.splitext(e.name)[1].lower()
            unique_filename = f"{uuid.uuid4()}{file_extension}"
            file_path = os.path.join(settings.upload_dir, unique_filename)
            
            # Save uploaded file
            with open(file_path, 'wb') as f:
                f.write(e.content.read())
            
            # Update file info display
            self._show_file_info(e.name, len(e.content.read()))
            
            # Trigger upload callback
            await self.on_upload(file_path)
            
            ui.notify('Image uploaded successfully!', type='positive')
            
        except Exception as error:
            ui.notify(f'Upload failed: {str(error)}', type='negative')
    
    def _is_valid_image(self, filename: str) -> bool:
        """Check if the uploaded file is a valid image."""
        if not filename:
            return False
        
        extension = os.path.splitext(filename)[1].lower().lstrip('.')
        return extension in settings.allowed_extensions
    
    def _show_file_info(self, filename: str, file_size: int):
        """Display information about the uploaded file."""
        self.file_info.style('display: flex;')
        self.file_name_label.text = filename
        
        # Format file size
        if file_size < 1024:
            size_str = f"{file_size} B"
        elif file_size < 1024 * 1024:
            size_str = f"{file_size / 1024:.1f} KB"
        else:
            size_str = f"{file_size / (1024 * 1024):.1f} MB"
        
        self.file_size_label.text = f"({size_str})"
    
    def reset(self):
        """Reset the upload component to initial state."""
        self.file_info.style('display: none;')
        self.file_name_label.text = ''
        self.file_size_label.text = ''