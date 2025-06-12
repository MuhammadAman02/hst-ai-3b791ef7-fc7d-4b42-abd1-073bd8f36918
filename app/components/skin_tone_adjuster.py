import asyncio
from typing import Dict, Any, Callable, Optional
import numpy as np
from nicegui import ui

class SkinToneAdjusterComponent:
    """Component for adjusting skin tone with real-time preview."""
    
    def __init__(self, on_adjust: Callable[[Dict[str, Any]], None]):
        self.on_adjust = on_adjust
        self.container = None
        self.current_image: Optional[np.ndarray] = None
        self.adjustments = {
            'brightness': 0,
            'warmth': 0,
            'saturation': 0,
            'hue_shift': 0
        }
        self.create_component()
    
    def create_component(self):
        """Create the skin tone adjustment UI component."""
        self.container = ui.element('div').classes('w-full')
        
        with self.container:
            # Initial empty state
            with ui.element('div').classes('text-center p-8 text-gray-500'):
                ui.icon('tune').classes('text-4xl mb-4')
                ui.label('Upload an image to adjust skin tone').classes('text-lg')
    
    async def update_image(self, image: np.ndarray):
        """Update the component with a new image."""
        self.current_image = image
        await self._create_adjustment_controls()
    
    async def _create_adjustment_controls(self):
        """Create the adjustment control interface."""
        try:
            # Clear existing content
            self.container.clear()
            
            with self.container:
                ui.label('Fine-tune your skin tone for more accurate color analysis').classes('text-gray-600 mb-6')
                
                with ui.row().classes('w-full gap-8'):
                    # Adjustment controls
                    with ui.column().classes('flex-1'):
                        ui.label('Adjustment Controls').classes('text-lg font-semibold mb-4')
                        
                        # Brightness control
                        with ui.card().classes('p-4 mb-4'):
                            ui.label('💡 Brightness').classes('font-medium mb-2')
                            brightness_slider = ui.slider(
                                min=-50, max=50, value=0, step=1
                            ).classes('w-full').props('label-always')
                            brightness_slider.on('update:model-value', lambda e: self._update_adjustment('brightness', e.args))
                            ui.label('Adjust overall lightness of your skin tone').classes('text-sm text-gray-500 mt-1')
                        
                        # Warmth control
                        with ui.card().classes('p-4 mb-4'):
                            ui.label('🌡️ Warmth').classes('font-medium mb-2')
                            warmth_slider = ui.slider(
                                min=-50, max=50, value=0, step=1
                            ).classes('w-full').props('label-always')
                            warmth_slider.on('update:model-value', lambda e: self._update_adjustment('warmth', e.args))
                            ui.label('Make skin tone warmer (yellow) or cooler (blue)').classes('text-sm text-gray-500 mt-1')
                        
                        # Saturation control
                        with ui.card().classes('p-4 mb-4'):
                            ui.label('🎨 Saturation').classes('font-medium mb-2')
                            saturation_slider = ui.slider(
                                min=-50, max=50, value=0, step=1
                            ).classes('w-full').props('label-always')
                            saturation_slider.on('update:model-value', lambda e: self._update_adjustment('saturation', e.args))
                            ui.label('Adjust color intensity and vibrancy').classes('text-sm text-gray-500 mt-1')
                        
                        # Hue shift control
                        with ui.card().classes('p-4 mb-4'):
                            ui.label('🌈 Hue Shift').classes('font-medium mb-2')
                            hue_slider = ui.slider(
                                min=-30, max=30, value=0, step=1
                            ).classes('w-full').props('label-always')
                            hue_slider.on('update:model-value', lambda e: self._update_adjustment('hue_shift', e.args))
                            ui.label('Shift the overall color hue').classes('text-sm text-gray-500 mt-1')
                        
                        # Control buttons
                        with ui.row().classes('gap-3 mt-6'):
                            ui.button('Reset All', on_click=self._reset_adjustments).props('flat color="grey"')
                            ui.button('Apply Changes', on_click=self._apply_adjustments).props('color="primary"')
                    
                    # Preset adjustments
                    with ui.column().classes('flex-1'):
                        ui.label('Quick Presets').classes('text-lg font-semibold mb-4')
                        
                        presets = [
                            {
                                'name': '☀️ Warmer Tone',
                                'description': 'Add golden warmth',
                                'adjustments': {'brightness': 5, 'warmth': 15, 'saturation': 5, 'hue_shift': 0}
                            },
                            {
                                'name': '❄️ Cooler Tone', 
                                'description': 'Add cool undertones',
                                'adjustments': {'brightness': 0, 'warmth': -15, 'saturation': 0, 'hue_shift': 0}
                            },
                            {
                                'name': '✨ Brighter',
                                'description': 'Increase brightness',
                                'adjustments': {'brightness': 20, 'warmth': 0, 'saturation': 10, 'hue_shift': 0}
                            },
                            {
                                'name': '🌙 Softer',
                                'description': 'Soften and mute',
                                'adjustments': {'brightness': -10, 'warmth': 0, 'saturation': -15, 'hue_shift': 0}
                            },
                            {
                                'name': '🌺 Enhanced',
                                'description': 'Boost vibrancy',
                                'adjustments': {'brightness': 10, 'warmth': 5, 'saturation': 20, 'hue_shift': 0}
                            }
                        ]
                        
                        for preset in presets:
                            with ui.card().classes('p-4 mb-3 cursor-pointer hover:shadow-md transition-shadow'):
                                ui.label(preset['name']).classes('font-medium mb-1')
                                ui.label(preset['description']).classes('text-sm text-gray-600 mb-3')
                                ui.button(
                                    'Apply Preset',
                                    on_click=lambda p=preset: self._apply_preset(p['adjustments'])
                                ).props('flat color="primary" size="sm"').classes('w-full')
                
                # Current adjustment values display
                with ui.card().classes('w-full p-4 mt-6 bg-gray-50'):
                    ui.label('Current Adjustments').classes('font-medium mb-3')
                    self.adjustment_display = ui.element('div')
                    self._update_adjustment_display()
                
        except Exception as e:
            self.container.clear()
            with self.container:
                ui.label(f'Error creating adjustment controls: {str(e)}').classes('text-red-500')
            print(f"Error creating adjustment controls: {e}")
    
    def _update_adjustment(self, adjustment_type: str, value):
        """Update a specific adjustment value."""
        self.adjustments[adjustment_type] = value
        self._update_adjustment_display()
    
    def _update_adjustment_display(self):
        """Update the current adjustments display."""
        if hasattr(self, 'adjustment_display'):
            self.adjustment_display.clear()
            with self.adjustment_display:
                with ui.grid(columns=4).classes('gap-3'):
                    for key, value in self.adjustments.items():
                        with ui.element('div').classes('text-center'):
                            ui.label(key.replace('_', ' ').title()).classes('text-sm font-medium')
                            ui.label(f'{value:+d}').classes('text-lg font-bold text-primary')
    
    async def _apply_adjustments(self):
        """Apply the current adjustments."""
        try:
            if self.current_image is not None:
                await self.on_adjust(self.adjustments.copy())
                ui.notify('🎨 Adjustments applied successfully!', type='positive')
            else:
                ui.notify('❌ No image to adjust', type='negative')
        except Exception as e:
            ui.notify(f'❌ Error applying adjustments: {str(e)}', type='negative')
            print(f"Error applying adjustments: {e}")
    
    def _reset_adjustments(self):
        """Reset all adjustments to default values."""
        self.adjustments = {
            'brightness': 0,
            'warmth': 0,
            'saturation': 0,
            'hue_shift': 0
        }
        self._update_adjustment_display()
        ui.notify('🔄 Adjustments reset to default', type='info')
    
    def _apply_preset(self, preset_adjustments: Dict[str, int]):
        """Apply a preset adjustment configuration."""
        self.adjustments.update(preset_adjustments)
        self._update_adjustment_display()
        ui.notify('✨ Preset applied! Click "Apply Changes" to see results.', type='info')