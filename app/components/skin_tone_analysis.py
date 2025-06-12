import base64
import io
from typing import Dict, Any, Optional
import numpy as np
from PIL import Image
from nicegui import ui

class SkinToneAnalysisComponent:
    """Component for displaying skin tone analysis results."""
    
    def __init__(self):
        self.container = None
        self.create_component()
    
    def create_component(self):
        """Create the skin tone analysis UI component."""
        self.container = ui.element('div').classes('w-full')
        
        with self.container:
            # Initial empty state
            with ui.element('div').classes('text-center p-8 text-gray-500'):
                ui.icon('analytics').classes('text-4xl mb-4')
                ui.label('Upload an image to see skin tone analysis').classes('text-lg')
    
    async def update_analysis(self, analysis_results: Dict[str, Any], image: np.ndarray):
        """Update the component with analysis results."""
        try:
            # Clear existing content
            self.container.clear()
            
            with self.container:
                with ui.row().classes('w-full gap-6'):
                    # Image display
                    with ui.column().classes('flex-1'):
                        ui.label('Analyzed Image').classes('text-lg font-semibold mb-3')
                        
                        # Convert numpy array to base64 for display
                        image_base64 = self._numpy_to_base64(image)
                        ui.image(f'data:image/jpeg;base64,{image_base64}').classes('w-full max-w-md rounded-lg shadow-md')
                    
                    # Analysis results
                    with ui.column().classes('flex-1'):
                        ui.label('Analysis Results').classes('text-lg font-semibold mb-3')
                        
                        # Skin tone information
                        with ui.card().classes('w-full p-4'):
                            # Primary color
                            with ui.row().classes('items-center gap-3 mb-3'):
                                ui.element('div').style(f'width: 40px; height: 40px; background-color: {analysis_results["primary_color"]}; border-radius: 8px; border: 2px solid #ddd;')
                                with ui.column().classes('gap-1'):
                                    ui.label('Primary Skin Tone').classes('font-medium')
                                    ui.label(analysis_results["primary_color"]).classes('text-sm text-gray-600 font-mono')
                            
                            # Category and undertone
                            with ui.grid(columns=2).classes('gap-4 mb-3'):
                                with ui.card().classes('p-3 bg-blue-50'):
                                    ui.label('Category').classes('text-sm font-medium text-blue-700')
                                    ui.label(analysis_results["category"]).classes('text-lg font-semibold text-blue-900')
                                
                                with ui.card().classes('p-3 bg-purple-50'):
                                    ui.label('Undertone').classes('text-sm font-medium text-purple-700')
                                    ui.label(analysis_results["undertone"].title()).classes('text-lg font-semibold text-purple-900')
                            
                            # Confidence score
                            confidence = analysis_results.get("confidence", 0.0)
                            confidence_percent = int(confidence * 100)
                            
                            ui.label(f'Analysis Confidence: {confidence_percent}%').classes('font-medium mb-2')
                            
                            # Confidence bar
                            with ui.element('div').classes('w-full bg-gray-200 rounded-full h-3'):
                                confidence_color = 'bg-green-500' if confidence > 0.8 else 'bg-yellow-500' if confidence > 0.6 else 'bg-red-500'
                                ui.element('div').classes(f'{confidence_color} h-3 rounded-full transition-all duration-500').style(f'width: {confidence_percent}%;')
                            
                            # RGB values
                            if "rgb_values" in analysis_results:
                                rgb = analysis_results["rgb_values"]
                                ui.label(f'RGB: ({rgb[0]}, {rgb[1]}, {rgb[2]})').classes('text-sm text-gray-600 mt-3 font-mono')
                            
                            # Analysis metadata
                            if "analysis_metadata" in analysis_results:
                                metadata = analysis_results["analysis_metadata"]
                                with ui.expansion('Technical Details').classes('mt-3'):
                                    ui.label(f'Pixels Analyzed: {metadata.get("pixels_analyzed", "N/A"):,}').classes('text-sm')
                                    if "color_variance" in metadata:
                                        variance = metadata["color_variance"]
                                        ui.label(f'Color Variance: R:{variance[0]:.1f}, G:{variance[1]:.1f}, B:{variance[2]:.1f}').classes('text-sm font-mono')
            
            # Skin tone characteristics
            await self._add_skin_tone_characteristics(analysis_results)
            
        except Exception as e:
            self.container.clear()
            with self.container:
                ui.label(f'Error displaying analysis: {str(e)}').classes('text-red-500')
            print(f"Error updating analysis component: {e}")
    
    async def _add_skin_tone_characteristics(self, analysis_results: Dict[str, Any]):
        """Add detailed skin tone characteristics."""
        category = analysis_results.get("category", "Medium")
        undertone = analysis_results.get("undertone", "neutral")
        
        # Characteristics based on skin tone
        characteristics = self._get_skin_tone_characteristics(category, undertone)
        
        with self.container:
            ui.separator().classes('my-6')
            
            ui.label('Skin Tone Characteristics').classes('text-lg font-semibold mb-4')
            
            with ui.grid(columns=1).classes('gap-4'):
                for char in characteristics:
                    with ui.card().classes('p-4 border-l-4 border-primary'):
                        ui.label(char["title"]).classes('font-medium text-primary mb-2')
                        ui.label(char["description"]).classes('text-gray-700')
    
    def _get_skin_tone_characteristics(self, category: str, undertone: str) -> list:
        """Get characteristics based on skin tone category and undertone."""
        characteristics = []
        
        # Category-based characteristics
        category_info = {
            "Very Light": {
                "title": "Fair Complexion",
                "description": "Your very light skin tone has delicate coloring that works beautifully with soft, muted colors and pastels."
            },
            "Light": {
                "title": "Light Complexion", 
                "description": "Your light skin tone has a luminous quality that pairs well with both soft and vibrant colors."
            },
            "Light-Medium": {
                "title": "Light-Medium Complexion",
                "description": "Your balanced skin tone offers versatility, working well with a wide range of color intensities."
            },
            "Medium": {
                "title": "Medium Complexion",
                "description": "Your medium skin tone has natural warmth that complements both earthy and vibrant color palettes."
            },
            "Medium-Dark": {
                "title": "Medium-Dark Complexion",
                "description": "Your rich skin tone has depth that looks stunning with bold, saturated colors and jewel tones."
            },
            "Dark": {
                "title": "Dark Complexion",
                "description": "Your deep skin tone has beautiful richness that shines with vibrant, high-contrast colors."
            },
            "Very Dark": {
                "title": "Very Dark Complexion",
                "description": "Your very dark skin tone has striking depth that looks magnificent with bright, bold colors and metallics."
            }
        }
        
        if category in category_info:
            characteristics.append(category_info[category])
        
        # Undertone-based characteristics
        undertone_info = {
            "warm": {
                "title": "Warm Undertones",
                "description": "Your warm undertones have golden, yellow, or peachy hues that work best with earth tones, warm reds, and golden colors."
            },
            "cool": {
                "title": "Cool Undertones", 
                "description": "Your cool undertones have pink, red, or blue hues that complement jewel tones, blues, and silver-based colors."
            },
            "neutral": {
                "title": "Neutral Undertones",
                "description": "Your balanced undertones give you the flexibility to wear both warm and cool colors beautifully."
            }
        }
        
        if undertone in undertone_info:
            characteristics.append(undertone_info[undertone])
        
        return characteristics
    
    def _numpy_to_base64(self, image: np.ndarray) -> str:
        """Convert numpy array to base64 string for display."""
        try:
            # Convert to PIL Image
            pil_image = Image.fromarray(image.astype('uint8'))
            
            # Convert to base64
            buffer = io.BytesIO()
            pil_image.save(buffer, format='JPEG', quality=85)
            image_base64 = base64.b64encode(buffer.getvalue()).decode()
            
            return image_base64
        except Exception as e:
            print(f"Error converting image to base64: {e}")
            return ""