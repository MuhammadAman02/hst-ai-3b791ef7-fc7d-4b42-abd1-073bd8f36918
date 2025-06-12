from nicegui import ui
from typing import Dict, Any, Optional

class SkinAnalysisComponent:
    """Component for displaying skin tone analysis results."""
    
    def __init__(self, visible: bool = False):
        self.visible = visible
        self.container = None
        self.skin_tone_data = None
        self.create_component()
    
    def create_component(self):
        """Create the skin analysis display component."""
        self.container = ui.card().classes('content-card w-full')
        
        with self.container:
            ui.label('🔍 Skin Tone Analysis').classes('section-title')
            
            # Analysis results container
            self.results_container = ui.column().classes('w-full gap-4')
            
            if not self.visible:
                self.container.style('display: none;')
    
    def update_analysis(self, skin_tone_data: Dict[str, Any]):
        """Update the component with new skin tone analysis data."""
        self.skin_tone_data = skin_tone_data
        self._render_analysis_results()
        self.show()
    
    def _render_analysis_results(self):
        """Render the skin tone analysis results."""
        if not self.skin_tone_data:
            return
        
        # Clear previous results
        self.results_container.clear()
        
        with self.results_container:
            # Primary skin tone
            with ui.row().classes('w-full items-center gap-4 p-4 bg-gray-50 rounded-lg'):
                # Skin tone color swatch
                primary_color = self.skin_tone_data.get('primary_color', '#D4A574')
                ui.element('div').style(
                    f'width: 60px; height: 60px; background-color: {primary_color}; '
                    'border-radius: 50%; border: 3px solid white; box-shadow: 0 4px 8px rgba(0,0,0,0.2);'
                )
                
                with ui.column().classes('flex-1'):
                    ui.label('Primary Skin Tone').classes('font-semibold text-gray-700')
                    ui.label(primary_color.upper()).classes('text-sm text-gray-500 font-mono')
                    
                    # Undertone classification
                    undertone = self.skin_tone_data.get('undertone', 'neutral')
                    undertone_color = self._get_undertone_color(undertone)
                    ui.label(f'Undertone: {undertone.title()}').classes(f'text-sm font-medium {undertone_color}')
            
            # Skin tone category
            category = self.skin_tone_data.get('category', 'Medium')
            confidence = self.skin_tone_data.get('confidence', 0.85)
            
            with ui.row().classes('w-full items-center justify-between p-4 bg-blue-50 rounded-lg'):
                with ui.column():
                    ui.label('Skin Tone Category').classes('font-semibold text-gray-700')
                    ui.label(category).classes('text-lg font-bold text-blue-600')
                
                with ui.column().classes('items-end'):
                    ui.label('Confidence').classes('text-sm text-gray-600')
                    ui.label(f'{confidence:.1%}').classes('text-lg font-bold text-green-600')
            
            # Color harmony information
            self._render_harmony_info()
    
    def _render_harmony_info(self):
        """Render color harmony information based on skin tone."""
        if not self.skin_tone_data:
            return
        
        undertone = self.skin_tone_data.get('undertone', 'neutral')
        
        with ui.card().classes('w-full p-4 mt-4'):
            ui.label('💡 Color Harmony Tips').classes('font-semibold text-gray-700 mb-2')
            
            tips = self._get_harmony_tips(undertone)
            for tip in tips:
                with ui.row().classes('items-start gap-2 mb-2'):
                    ui.icon('check_circle', size='sm').classes('text-green-500 mt-1')
                    ui.label(tip).classes('text-sm text-gray-600')
    
    def _get_undertone_color(self, undertone: str) -> str:
        """Get CSS class for undertone color coding."""
        color_map = {
            'warm': 'text-orange-600',
            'cool': 'text-blue-600',
            'neutral': 'text-purple-600'
        }
        return color_map.get(undertone, 'text-gray-600')
    
    def _get_harmony_tips(self, undertone: str) -> list:
        """Get color harmony tips based on undertone."""
        tips_map = {
            'warm': [
                'Earth tones like terracotta, warm browns, and golden yellows complement your skin',
                'Coral, peach, and warm reds are excellent choices',
                'Avoid cool blues and stark whites - opt for cream and ivory instead'
            ],
            'cool': [
                'Cool blues, purples, and emerald greens enhance your natural coloring',
                'True whites, black, and silver tones work beautifully',
                'Pink-based colors and jewel tones are particularly flattering'
            ],
            'neutral': [
                'You have the flexibility to wear both warm and cool colors',
                'Soft, muted tones and balanced colors work well',
                'Experiment with both gold and silver accessories'
            ]
        }
        return tips_map.get(undertone, ['Your skin tone is unique and beautiful!'])
    
    def show(self):
        """Show the analysis component."""
        self.container.style('display: block;')
        self.visible = True
    
    def hide(self):
        """Hide the analysis component."""
        self.container.style('display: none;')
        self.visible = False
    
    def clear(self):
        """Clear the analysis results."""
        self.results_container.clear()
        self.skin_tone_data = None