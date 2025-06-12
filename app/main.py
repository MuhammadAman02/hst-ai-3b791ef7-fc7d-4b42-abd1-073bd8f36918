from nicegui import ui, app
from app.components.image_upload import ImageUploadComponent
from app.components.skin_analysis import SkinAnalysisComponent
from app.components.color_recommendations import ColorRecommendationsComponent
from app.components.skin_tone_adjuster import SkinToneAdjusterComponent
from app.services.image_service import ImageService
from app.services.color_service import ColorService
import asyncio

# Initialize services
image_service = ImageService()
color_service = ColorService()

# Global state for the application
class AppState:
    def __init__(self):
        self.current_image = None
        self.original_image = None
        self.skin_tone_data = None
        self.color_recommendations = None
        self.processing = False

app_state = AppState()

@ui.page('/')
async def main_page():
    """Main application page with color analysis functionality."""
    
    # Add custom CSS for beautiful styling
    ui.add_head_html('''
    <style>
        .main-container {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .app-header {
            text-align: center;
            color: white;
            margin-bottom: 30px;
        }
        
        .app-title {
            font-size: 3rem;
            font-weight: 700;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .app-subtitle {
            font-size: 1.2rem;
            opacity: 0.9;
            font-weight: 300;
        }
        
        .content-card {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            backdrop-filter: blur(10px);
            margin-bottom: 20px;
        }
        
        .section-title {
            font-size: 1.5rem;
            font-weight: 600;
            color: #4a5568;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .processing-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.7);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 1000;
            color: white;
            font-size: 1.2rem;
        }
        
        .color-swatch {
            width: 60px;
            height: 60px;
            border-radius: 12px;
            border: 3px solid white;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            cursor: pointer;
            transition: transform 0.2s;
        }
        
        .color-swatch:hover {
            transform: scale(1.1);
        }
        
        .skin-tone-preview {
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 10px 20px rgba(0,0,0,0.2);
        }
        
        .recommendation-card {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            border-radius: 15px;
            padding: 20px;
            margin: 10px 0;
        }
        
        .cool-tone-card {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        }
        
        .warm-tone-card {
            background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        }
        
        .neutral-tone-card {
            background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
            color: #4a5568;
        }
    </style>
    ''')
    
    with ui.column().classes('main-container w-full'):
        # Header
        with ui.column().classes('app-header'):
            ui.label('🎨 Color Harmony').classes('app-title')
            ui.label('AI-Powered Skin Tone & Color Analysis').classes('app-subtitle')
        
        # Main content area
        with ui.row().classes('w-full gap-6 justify-center'):
            # Left column - Image upload and processing
            with ui.column().classes('w-full max-w-md'):
                with ui.card().classes('content-card'):
                    ui.label('📸 Upload Your Photo').classes('section-title')
                    
                    # Image upload component
                    upload_component = ImageUploadComponent(
                        on_upload=handle_image_upload,
                        max_size=10*1024*1024
                    )
                    
                    # Current image display
                    image_display = ui.image().classes('w-full skin-tone-preview').style('display: none;')
                    
                    # Skin tone adjuster
                    adjuster_component = SkinToneAdjusterComponent(
                        on_adjust=handle_skin_tone_adjustment,
                        visible=False
                    )
            
            # Right column - Analysis results
            with ui.column().classes('w-full max-w-md'):
                # Skin analysis results
                analysis_component = SkinAnalysisComponent(visible=False)
                
                # Color recommendations
                recommendations_component = ColorRecommendationsComponent(visible=False)
        
        # Processing overlay
        processing_overlay = ui.element('div').classes('processing-overlay').style('display: none;')
        with processing_overlay:
            with ui.column().classes('items-center gap-4'):
                ui.spinner(size='lg')
                ui.label('Analyzing your skin tone and generating color recommendations...')

async def handle_image_upload(file_path: str):
    """Handle uploaded image and trigger analysis."""
    try:
        app_state.processing = True
        show_processing_overlay()
        
        # Process the uploaded image
        app_state.original_image = await image_service.load_image(file_path)
        app_state.current_image = app_state.original_image.copy()
        
        # Perform skin tone analysis
        app_state.skin_tone_data = await color_service.analyze_skin_tone(app_state.current_image)
        
        # Generate color recommendations
        app_state.color_recommendations = await color_service.get_color_recommendations(
            app_state.skin_tone_data
        )
        
        # Update UI components
        await update_ui_after_analysis()
        
    except Exception as e:
        ui.notify(f'Error processing image: {str(e)}', type='negative')
    finally:
        app_state.processing = False
        hide_processing_overlay()

async def handle_skin_tone_adjustment(adjustment_params: dict):
    """Handle skin tone adjustment parameters."""
    if app_state.original_image is None:
        return
    
    try:
        app_state.processing = True
        show_processing_overlay()
        
        # Apply skin tone adjustments
        app_state.current_image = await image_service.adjust_skin_tone(
            app_state.original_image,
            adjustment_params
        )
        
        # Re-analyze with adjusted image
        app_state.skin_tone_data = await color_service.analyze_skin_tone(app_state.current_image)
        app_state.color_recommendations = await color_service.get_color_recommendations(
            app_state.skin_tone_data
        )
        
        # Update UI
        await update_ui_after_analysis()
        
    except Exception as e:
        ui.notify(f'Error adjusting skin tone: {str(e)}', type='negative')
    finally:
        app_state.processing = False
        hide_processing_overlay()

async def update_ui_after_analysis():
    """Update all UI components after image analysis."""
    # This would update the reactive components
    # Implementation depends on the specific component architecture
    pass

def show_processing_overlay():
    """Show the processing overlay."""
    # Implementation for showing overlay
    pass

def hide_processing_overlay():
    """Hide the processing overlay."""
    # Implementation for hiding overlay
    pass

@ui.page('/health')
async def health_check():
    """Health check endpoint for deployment monitoring."""
    return {'status': 'healthy', 'service': 'color-harmony-api'}