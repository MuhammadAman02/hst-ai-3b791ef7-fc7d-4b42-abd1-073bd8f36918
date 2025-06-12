import asyncio
import os
import uuid
from typing import Optional, Dict, Any
from nicegui import ui, app, events
import numpy as np

from app.config import settings
from app.components.image_upload import ImageUploadComponent
from app.components.skin_tone_analysis import SkinToneAnalysisComponent
from app.components.color_recommendations import ColorRecommendationsComponent
from app.components.skin_tone_adjuster import SkinToneAdjusterComponent
from app.services.color_service import ColorService
from app.services.image_service import ImageService

# Initialize services
color_service = ColorService()
image_service = ImageService()

# Global state for the application
class AppState:
    def __init__(self):
        self.current_image: Optional[np.ndarray] = None
        self.original_image: Optional[np.ndarray] = None
        self.analysis_results: Optional[Dict[str, Any]] = None
        self.color_recommendations: Optional[Dict[str, Any]] = None
        self.uploaded_filename: Optional[str] = None
        self.processing: bool = False

app_state = AppState()

@ui.page('/')
async def main_page():
    """Main application page."""
    
    # Custom CSS for the application
    ui.add_head_html('''
    <style>
        .main-container {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .content-card {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            padding: 30px;
            margin: 20px auto;
            max-width: 1200px;
        }
        
        .header-title {
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-size: 2.5rem;
            font-weight: bold;
            text-align: center;
            margin-bottom: 10px;
        }
        
        .header-subtitle {
            color: #666;
            text-align: center;
            font-size: 1.1rem;
            margin-bottom: 30px;
        }
        
        .section-card {
            background: white;
            border-radius: 15px;
            padding: 25px;
            margin: 20px 0;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
            border: 1px solid rgba(0, 0, 0, 0.05);
        }
        
        .section-title {
            color: #333;
            font-size: 1.4rem;
            font-weight: 600;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .loading-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.7);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 1000;
        }
        
        .loading-content {
            background: white;
            padding: 30px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        }
        
        .error-message {
            background: #fee;
            border: 1px solid #fcc;
            color: #c33;
            padding: 15px;
            border-radius: 10px;
            margin: 10px 0;
        }
        
        .success-message {
            background: #efe;
            border: 1px solid #cfc;
            color: #3c3;
            padding: 15px;
            border-radius: 10px;
            margin: 10px 0;
        }
    </style>
    ''')
    
    # Loading overlay
    loading_overlay = ui.element('div').classes('loading-overlay').style('display: none;')
    with loading_overlay:
        with ui.element('div').classes('loading-content'):
            ui.spinner(size='lg')
            ui.label('Analyzing your image...').classes('text-lg mt-4')
    
    # Main container
    with ui.element('div').classes('main-container'):
        with ui.element('div').classes('content-card'):
            # Header
            ui.html('<h1 class="header-title">🎨 Color Harmony</h1>')
            ui.html('<p class="header-subtitle">Discover your perfect colors with AI-powered skin tone analysis</p>')
            
            # Image Upload Section
            with ui.element('div').classes('section-card'):
                ui.html('<h2 class="section-title">📸 Upload Your Photo</h2>')
                upload_component = ImageUploadComponent(on_upload=handle_image_upload)
            
            # Analysis Results Section
            analysis_container = ui.element('div').style('display: none;')
            with analysis_container:
                with ui.element('div').classes('section-card'):
                    ui.html('<h2 class="section-title">🔍 Skin Tone Analysis</h2>')
                    analysis_component = SkinToneAnalysisComponent()
                
                with ui.element('div').classes('section-card'):
                    ui.html('<h2 class="section-title">🎨 Color Recommendations</h2>')
                    recommendations_component = ColorRecommendationsComponent()
                
                with ui.element('div').classes('section-card'):
                    ui.html('<h2 class="section-title">🎛️ Adjust Skin Tone</h2>')
                    adjuster_component = SkinToneAdjusterComponent(on_adjust=handle_skin_tone_adjustment)
    
    async def handle_image_upload(file_path: str, filename: str):
        """Handle image upload and analysis."""
        try:
            # Show loading overlay
            loading_overlay.style('display: flex;')
            app_state.processing = True
            
            # Load and process image
            app_state.original_image = await image_service.load_image(file_path)
            app_state.current_image = app_state.original_image.copy()
            app_state.uploaded_filename = filename
            
            # Perform skin tone analysis
            app_state.analysis_results = await color_service.analyze_skin_tone(app_state.current_image)
            
            # Get color recommendations
            app_state.color_recommendations = await color_service.get_color_recommendations(app_state.analysis_results)
            
            # Update UI components
            await analysis_component.update_analysis(app_state.analysis_results, app_state.current_image)
            await recommendations_component.update_recommendations(app_state.color_recommendations)
            await adjuster_component.update_image(app_state.current_image)
            
            # Show analysis results
            analysis_container.style('display: block;')
            
            # Hide loading overlay
            loading_overlay.style('display: none;')
            app_state.processing = False
            
            ui.notify('✅ Analysis complete! Scroll down to see your results.', type='positive')
            
        except Exception as e:
            loading_overlay.style('display: none;')
            app_state.processing = False
            ui.notify(f'❌ Error analyzing image: {str(e)}', type='negative')
            print(f"Error in image analysis: {e}")
    
    async def handle_skin_tone_adjustment(adjustments: Dict[str, Any]):
        """Handle skin tone adjustments."""
        try:
            if app_state.original_image is None:
                return
            
            # Apply adjustments to original image
            app_state.current_image = await image_service.adjust_skin_tone(
                app_state.original_image, adjustments
            )
            
            # Re-analyze with adjusted image
            app_state.analysis_results = await color_service.analyze_skin_tone(app_state.current_image)
            app_state.color_recommendations = await color_service.get_color_recommendations(app_state.analysis_results)
            
            # Update UI components
            await analysis_component.update_analysis(app_state.analysis_results, app_state.current_image)
            await recommendations_component.update_recommendations(app_state.color_recommendations)
            
            ui.notify('🎨 Skin tone adjusted successfully!', type='positive')
            
        except Exception as e:
            ui.notify(f'❌ Error adjusting skin tone: {str(e)}', type='negative')
            print(f"Error in skin tone adjustment: {e}")

@ui.page('/health')
async def health_check():
    """Health check endpoint for deployment."""
    return {'status': 'healthy', 'service': 'Color Harmony API'}

# Error handling for the application
app.on_exception(lambda e: ui.notify(f'Application error: {str(e)}', type='negative'))