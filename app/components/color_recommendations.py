from typing import Dict, Any, List
from nicegui import ui

class ColorRecommendationsComponent:
    """Component for displaying color recommendations."""
    
    def __init__(self):
        self.container = None
        self.create_component()
    
    def create_component(self):
        """Create the color recommendations UI component."""
        self.container = ui.element('div').classes('w-full')
        
        with self.container:
            # Initial empty state
            with ui.element('div').classes('text-center p-8 text-gray-500'):
                ui.icon('palette').classes('text-4xl mb-4')
                ui.label('Color recommendations will appear here after analysis').classes('text-lg')
    
    async def update_recommendations(self, recommendations: Dict[str, Any]):
        """Update the component with color recommendations."""
        try:
            # Clear existing content
            self.container.clear()
            
            with self.container:
                # Best colors section
                if recommendations.get("best_colors"):
                    await self._create_color_section(
                        "✨ Colors That Enhance Your Beauty",
                        recommendations["best_colors"],
                        "These colors will make your skin glow and bring out your natural radiance.",
                        "bg-green-50",
                        "text-green-700"
                    )
                
                # Seasonal palette
                if recommendations.get("seasonal_palette"):
                    await self._create_seasonal_section(recommendations["seasonal_palette"])
                
                # Outfit suggestions
                if recommendations.get("outfit_suggestions"):
                    await self._create_outfit_section(recommendations["outfit_suggestions"])
                
                # Colors to avoid (if any)
                if recommendations.get("avoid_colors"):
                    await self._create_color_section(
                        "⚠️ Colors to Use Sparingly",
                        recommendations["avoid_colors"],
                        "These colors may wash you out. Use them as small accents if desired.",
                        "bg-yellow-50",
                        "text-yellow-700"
                    )
                
        except Exception as e:
            self.container.clear()
            with self.container:
                ui.label(f'Error displaying recommendations: {str(e)}').classes('text-red-500')
            print(f"Error updating recommendations component: {e}")
    
    async def _create_color_section(self, title: str, colors: List[Dict], description: str, bg_class: str, text_class: str):
        """Create a section for displaying colors."""
        with ui.card().classes(f'w-full p-6 mb-6 {bg_class}'):
            ui.label(title).classes(f'text-xl font-bold {text_class} mb-3')
            ui.label(description).classes(f'{text_class} mb-4')
            
            # Color grid
            with ui.grid(columns=4).classes('gap-4 mb-4'):
                for color in colors[:12]:  # Limit to 12 colors
                    await self._create_color_card(color)
    
    async def _create_color_card(self, color: Dict[str, Any]):
        """Create a card for a single color."""
        with ui.card().classes('p-3 hover:shadow-lg transition-shadow cursor-pointer'):
            # Color swatch
            ui.element('div').style(
                f'width: 100%; height: 60px; background-color: {color["hex"]}; '
                f'border-radius: 8px; border: 2px solid #ddd; margin-bottom: 8px;'
            )
            
            # Color information
            ui.label(color.get("name", "Unknown")).classes('font-medium text-sm text-center')
            ui.label(color["hex"]).classes('text-xs text-gray-500 text-center font-mono')
            
            # Confidence indicator
            confidence = color.get("confidence", 0.5)
            confidence_percent = int(confidence * 100)
            
            with ui.row().classes('items-center justify-center gap-1 mt-2'):
                ui.icon('star').classes('text-xs text-yellow-500')
                ui.label(f'{confidence_percent}%').classes('text-xs text-gray-600')
            
            # Usage suggestion
            if color.get("usage"):
                ui.label(color["usage"]).classes('text-xs text-gray-500 text-center mt-1')
    
    async def _create_seasonal_section(self, seasonal_palette: Dict[str, Any]):
        """Create the seasonal palette section."""
        season = seasonal_palette.get("season", "Summer")
        colors = seasonal_palette.get("colors", [])
        description = seasonal_palette.get("description", "")
        
        with ui.card().classes('w-full p-6 mb-6 bg-purple-50'):
            ui.label(f'🌸 Your {season} Palette').classes('text-xl font-bold text-purple-700 mb-3')
            ui.label(description).classes('text-purple-700 mb-4')
            
            # Seasonal colors
            with ui.grid(columns=5).classes('gap-3'):
                for color_hex in colors:
                    with ui.element('div').classes('text-center'):
                        ui.element('div').style(
                            f'width: 50px; height: 50px; background-color: {color_hex}; '
                            f'border-radius: 50%; border: 3px solid white; box-shadow: 0 2px 8px rgba(0,0,0,0.1); '
                            f'margin: 0 auto 5px auto;'
                        )
                        ui.label(color_hex).classes('text-xs text-gray-600 font-mono')
    
    async def _create_outfit_section(self, outfit_suggestions: List[Dict[str, Any]]):
        """Create the outfit suggestions section."""
        if not outfit_suggestions:
            return
        
        with ui.card().classes('w-full p-6 mb-6 bg-blue-50'):
            ui.label('👗 Outfit Color Combinations').classes('text-xl font-bold text-blue-700 mb-3')
            ui.label('Try these harmonious color combinations for different occasions.').classes('text-blue-700 mb-4')
            
            with ui.grid(columns=1).classes('gap-4'):
                for outfit in outfit_suggestions:
                    await self._create_outfit_card(outfit)
    
    async def _create_outfit_card(self, outfit: Dict[str, Any]):
        """Create a card for an outfit suggestion."""
        with ui.card().classes('p-4 border border-blue-200'):
            # Outfit name and occasion
            with ui.row().classes('items-center justify-between mb-3'):
                ui.label(outfit.get("name", "Outfit Combination")).classes('font-semibold text-lg')
                ui.chip(outfit.get("occasion", "Casual")).classes('bg-blue-100 text-blue-700')
            
            # Color combination
            with ui.row().classes('items-center gap-3 mb-3'):
                for color_hex in outfit.get("colors", []):
                    ui.element('div').style(
                        f'width: 40px; height: 40px; background-color: {color_hex}; '
                        f'border-radius: 8px; border: 2px solid #ddd;'
                    )
                
                ui.icon('arrow_forward').classes('text-gray-400')
                ui.label('Perfect Harmony').classes('text-sm text-gray-600 italic')
            
            # Description
            if outfit.get("description"):
                ui.label(outfit["description"]).classes('text-gray-700 text-sm')