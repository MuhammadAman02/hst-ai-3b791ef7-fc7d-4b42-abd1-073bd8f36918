from nicegui import ui
from typing import Dict, List, Any

class ColorRecommendationsComponent:
    """Component for displaying personalized color recommendations."""
    
    def __init__(self, visible: bool = False):
        self.visible = visible
        self.container = None
        self.recommendations = None
        self.create_component()
    
    def create_component(self):
        """Create the color recommendations display component."""
        self.container = ui.card().classes('content-card w-full')
        
        with self.container:
            ui.label('🎨 Your Perfect Colors').classes('section-title')
            
            # Recommendations container
            self.recommendations_container = ui.column().classes('w-full gap-6')
            
            if not self.visible:
                self.container.style('display: none;')
    
    def update_recommendations(self, recommendations: Dict[str, Any]):
        """Update the component with new color recommendations."""
        self.recommendations = recommendations
        self._render_recommendations()
        self.show()
    
    def _render_recommendations(self):
        """Render the color recommendations."""
        if not self.recommendations:
            return
        
        # Clear previous recommendations
        self.recommendations_container.clear()
        
        with self.recommendations_container:
            # Best colors section
            self._render_color_category(
                'Best Colors for You',
                self.recommendations.get('best_colors', []),
                'recommendation-card'
            )
            
            # Colors to avoid section
            self._render_color_category(
                'Colors to Use Sparingly',
                self.recommendations.get('avoid_colors', []),
                'recommendation-card',
                is_avoid=True
            )
            
            # Seasonal palette
            if 'seasonal_palette' in self.recommendations:
                self._render_seasonal_palette()
            
            # Outfit suggestions
            if 'outfit_suggestions' in self.recommendations:
                self._render_outfit_suggestions()
    
    def _render_color_category(self, title: str, colors: List[Dict], card_class: str, is_avoid: bool = False):
        """Render a category of color recommendations."""
        if not colors:
            return
        
        icon = '❌' if is_avoid else '✨'
        
        with ui.card().classes(f'{card_class} w-full'):
            ui.label(f'{icon} {title}').classes('text-lg font-semibold mb-4')
            
            # Color grid
            with ui.grid(columns=4).classes('w-full gap-3'):
                for color_info in colors:
                    self._render_color_swatch(color_info, is_avoid)
    
    def _render_color_swatch(self, color_info: Dict, is_avoid: bool = False):
        """Render an individual color swatch with information."""
        color_hex = color_info.get('hex', '#000000')
        color_name = color_info.get('name', 'Unknown')
        confidence = color_info.get('confidence', 0.0)
        
        with ui.column().classes('items-center gap-2'):
            # Color swatch
            swatch_style = (
                f'width: 60px; height: 60px; background-color: {color_hex}; '
                'border-radius: 12px; border: 3px solid white; '
                'box-shadow: 0 4px 8px rgba(0,0,0,0.2); cursor: pointer; '
                'transition: transform 0.2s;'
            )
            
            if is_avoid:
                swatch_style += 'opacity: 0.6; filter: grayscale(20%);'
            
            color_swatch = ui.element('div').style(swatch_style)
            color_swatch.on('click', lambda c=color_info: self._show_color_details(c))
            
            # Color information
            ui.label(color_name).classes('text-xs font-medium text-center max-w-16 truncate')
            
            if confidence > 0:
                confidence_color = 'text-green-600' if confidence > 0.7 else 'text-yellow-600'
                ui.label(f'{confidence:.0%}').classes(f'text-xs {confidence_color}')
    
    def _render_seasonal_palette(self):
        """Render seasonal color palette recommendations."""
        seasonal_data = self.recommendations.get('seasonal_palette', {})
        season = seasonal_data.get('season', 'Unknown')
        colors = seasonal_data.get('colors', [])
        
        if not colors:
            return
        
        with ui.card().classes('w-full p-6 mt-4'):
            ui.label(f'🍂 Your Seasonal Palette: {season}').classes('text-lg font-semibold mb-4')
            
            # Season description
            description = self._get_season_description(season)
            ui.label(description).classes('text-sm text-gray-600 mb-4')
            
            # Seasonal colors
            with ui.grid(columns=6).classes('w-full gap-2'):
                for color in colors:
                    ui.element('div').style(
                        f'width: 40px; height: 40px; background-color: {color}; '
                        'border-radius: 8px; border: 2px solid white; '
                        'box-shadow: 0 2px 4px rgba(0,0,0,0.1);'
                    )
    
    def _render_outfit_suggestions(self):
        """Render outfit color combination suggestions."""
        suggestions = self.recommendations.get('outfit_suggestions', [])
        
        if not suggestions:
            return
        
        with ui.card().classes('w-full p-6 mt-4'):
            ui.label('👗 Outfit Color Combinations').classes('text-lg font-semibold mb-4')
            
            for i, suggestion in enumerate(suggestions[:3]):  # Show top 3 suggestions
                with ui.row().classes('w-full items-center gap-4 p-3 bg-gray-50 rounded-lg mb-3'):
                    # Color combination preview
                    with ui.row().classes('gap-1'):
                        for color in suggestion.get('colors', []):
                            ui.element('div').style(
                                f'width: 30px; height: 30px; background-color: {color}; '
                                'border-radius: 6px; border: 1px solid white;'
                            )
                    
                    # Suggestion details
                    with ui.column().classes('flex-1'):
                        ui.label(suggestion.get('name', f'Combination {i+1}')).classes('font-medium')
                        ui.label(suggestion.get('description', 'Great color harmony')).classes('text-sm text-gray-600')
    
    def _get_season_description(self, season: str) -> str:
        """Get description for seasonal color palette."""
        descriptions = {
            'Spring': 'Warm, clear, and bright colors that reflect the freshness of spring',
            'Summer': 'Cool, soft, and muted colors with blue undertones',
            'Autumn': 'Warm, rich, and earthy colors with golden undertones',
            'Winter': 'Cool, clear, and intense colors with blue undertones'
        }
        return descriptions.get(season, 'A beautiful palette of colors that complement your skin tone')
    
    def _show_color_details(self, color_info: Dict):
        """Show detailed information about a selected color."""
        color_name = color_info.get('name', 'Unknown')
        color_hex = color_info.get('hex', '#000000')
        
        # Create a dialog with color details
        with ui.dialog() as dialog, ui.card().classes('w-80'):
            with ui.column().classes('items-center gap-4 p-4'):
                # Large color swatch
                ui.element('div').style(
                    f'width: 100px; height: 100px; background-color: {color_hex}; '
                    'border-radius: 20px; border: 4px solid white; '
                    'box-shadow: 0 8px 16px rgba(0,0,0,0.2);'
                )
                
                ui.label(color_name).classes('text-xl font-semibold')
                ui.label(color_hex.upper()).classes('text-lg font-mono text-gray-600')
                
                # Usage suggestions
                usage = color_info.get('usage', 'Perfect for various styling options')
                ui.label(usage).classes('text-sm text-gray-600 text-center')
                
                ui.button('Close', on_click=dialog.close).classes('mt-4')
        
        dialog.open()
    
    def show(self):
        """Show the recommendations component."""
        self.container.style('display: block;')
        self.visible = True
    
    def hide(self):
        """Hide the recommendations component."""
        self.container.style('display: none;')
        self.visible = False
    
    def clear(self):
        """Clear the recommendations."""
        self.recommendations_container.clear()
        self.recommendations = None