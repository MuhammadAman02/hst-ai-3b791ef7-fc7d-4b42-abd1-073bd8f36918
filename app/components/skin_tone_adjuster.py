from nicegui import ui
from typing import Callable, Dict, Any

class SkinToneAdjusterComponent:
    """Component for adjusting skin tone parameters in real-time."""
    
    def __init__(self, on_adjust: Callable[[Dict[str, Any]], None], visible: bool = False):
        self.on_adjust = on_adjust
        self.visible = visible
        self.container = None
        self.adjustment_params = {
            'brightness': 0,
            'warmth': 0,
            'saturation': 0,
            'hue_shift': 0
        }
        self.create_component()
    
    def create_component(self):
        """Create the skin tone adjustment UI component."""
        self.container = ui.card().classes('content-card w-full mt-4')
        
        with self.container:
            ui.label('🎛️ Adjust Skin Tone').classes('section-title')
            
            with ui.column().classes('w-full gap-4'):
                # Brightness adjustment
                with ui.row().classes('w-full items-center gap-4'):
                    ui.icon('brightness_6').classes('text-gray-600')
                    ui.label('Brightness').classes('font-medium min-w-20')
                    self.brightness_slider = ui.slider(
                        min=-50, max=50, value=0, step=1
                    ).classes('flex-1').on('change', self._on_brightness_change)
                    self.brightness_value = ui.label('0').classes('min-w-8 text-right text-sm')
                
                # Warmth adjustment (temperature)
                with ui.row().classes('w-full items-center gap-4'):
                    ui.icon('thermostat').classes('text-gray-600')
                    ui.label('Warmth').classes('font-medium min-w-20')
                    self.warmth_slider = ui.slider(
                        min=-50, max=50, value=0, step=1
                    ).classes('flex-1').on('change', self._on_warmth_change)
                    self.warmth_value = ui.label('0').classes('min-w-8 text-right text-sm')
                
                # Saturation adjustment
                with ui.row().classes('w-full items-center gap-4'):
                    ui.icon('palette').classes('text-gray-600')
                    ui.label('Saturation').classes('font-medium min-w-20')
                    self.saturation_slider = ui.slider(
                        min=-50, max=50, value=0, step=1
                    ).classes('flex-1').on('change', self._on_saturation_change)
                    self.saturation_value = ui.label('0').classes('min-w-8 text-right text-sm')
                
                # Hue shift adjustment
                with ui.row().classes('w-full items-center gap-4'):
                    ui.icon('tune').classes('text-gray-600')
                    ui.label('Hue Shift').classes('font-medium min-w-20')
                    self.hue_slider = ui.slider(
                        min=-30, max=30, value=0, step=1
                    ).classes('flex-1').on('change', self._on_hue_change)
                    self.hue_value = ui.label('0').classes('min-w-8 text-right text-sm')
                
                # Control buttons
                with ui.row().classes('w-full justify-between mt-6'):
                    ui.button(
                        'Reset All',
                        icon='refresh',
                        on_click=self._reset_adjustments
                    ).classes('bg-gray-500 text-white')
                    
                    ui.button(
                        'Apply Changes',
                        icon='check',
                        on_click=self._apply_adjustments
                    ).classes('bg-blue-500 text-white')
                
                # Preset adjustments
                with ui.expansion('Quick Presets', icon='auto_fix_high').classes('w-full mt-4'):
                    with ui.grid(columns=2).classes('w-full gap-2 p-2'):
                        ui.button(
                            'Warmer Tone',
                            on_click=lambda: self._apply_preset('warmer')
                        ).classes('bg-orange-100 text-orange-700 hover:bg-orange-200')
                        
                        ui.button(
                            'Cooler Tone',
                            on_click=lambda: self._apply_preset('cooler')
                        ).classes('bg-blue-100 text-blue-700 hover:bg-blue-200')
                        
                        ui.button(
                            'Brighter',
                            on_click=lambda: self._apply_preset('brighter')
                        ).classes('bg-yellow-100 text-yellow-700 hover:bg-yellow-200')
                        
                        ui.button(
                            'More Vibrant',
                            on_click=lambda: self._apply_preset('vibrant')
                        ).classes('bg-pink-100 text-pink-700 hover:bg-pink-200')
        
        if not self.visible:
            self.container.style('display: none;')
    
    def _on_brightness_change(self, e):
        """Handle brightness slider change."""
        value = int(e.value)
        self.adjustment_params['brightness'] = value
        self.brightness_value.text = str(value)
    
    def _on_warmth_change(self, e):
        """Handle warmth slider change."""
        value = int(e.value)
        self.adjustment_params['warmth'] = value
        self.warmth_value.text = str(value)
    
    def _on_saturation_change(self, e):
        """Handle saturation slider change."""
        value = int(e.value)
        self.adjustment_params['saturation'] = value
        self.saturation_value.text = str(value)
    
    def _on_hue_change(self, e):
        """Handle hue shift slider change."""
        value = int(e.value)
        self.adjustment_params['hue_shift'] = value
        self.hue_value.text = str(value)
    
    def _reset_adjustments(self):
        """Reset all adjustments to default values."""
        self.adjustment_params = {
            'brightness': 0,
            'warmth': 0,
            'saturation': 0,
            'hue_shift': 0
        }
        
        # Update sliders
        self.brightness_slider.value = 0
        self.warmth_slider.value = 0
        self.saturation_slider.value = 0
        self.hue_slider.value = 0
        
        # Update value labels
        self.brightness_value.text = '0'
        self.warmth_value.text = '0'
        self.saturation_value.text = '0'
        self.hue_value.text = '0'
        
        ui.notify('Adjustments reset to default', type='info')
    
    def _apply_adjustments(self):
        """Apply the current adjustments."""
        self.on_adjust(self.adjustment_params.copy())
        ui.notify('Skin tone adjustments applied!', type='positive')
    
    def _apply_preset(self, preset_name: str):
        """Apply a preset adjustment configuration."""
        presets = {
            'warmer': {'brightness': 5, 'warmth': 20, 'saturation': 10, 'hue_shift': 5},
            'cooler': {'brightness': 0, 'warmth': -20, 'saturation': 5, 'hue_shift': -5},
            'brighter': {'brightness': 15, 'warmth': 5, 'saturation': 8, 'hue_shift': 0},
            'vibrant': {'brightness': 8, 'warmth': 0, 'saturation': 25, 'hue_shift': 0}
        }
        
        if preset_name in presets:
            preset = presets[preset_name]
            
            # Update adjustment parameters
            self.adjustment_params.update(preset)
            
            # Update sliders
            self.brightness_slider.value = preset['brightness']
            self.warmth_slider.value = preset['warmth']
            self.saturation_slider.value = preset['saturation']
            self.hue_slider.value = preset['hue_shift']
            
            # Update value labels
            self.brightness_value.text = str(preset['brightness'])
            self.warmth_value.text = str(preset['warmth'])
            self.saturation_value.text = str(preset['saturation'])
            self.hue_value.text = str(preset['hue_shift'])
            
            # Auto-apply the preset
            self.on_adjust(self.adjustment_params.copy())
            
            ui.notify(f'{preset_name.title()} preset applied!', type='positive')
    
    def show(self):
        """Show the adjuster component."""
        self.container.style('display: block;')
        self.visible = True
    
    def hide(self):
        """Hide the adjuster component."""
        self.container.style('display: none;')
        self.visible = False
    
    def get_current_adjustments(self) -> Dict[str, Any]:
        """Get the current adjustment parameters."""
        return self.adjustment_params.copy()
    
    def set_adjustments(self, adjustments: Dict[str, Any]):
        """Set adjustment parameters programmatically."""
        for key, value in adjustments.items():
            if key in self.adjustment_params:
                self.adjustment_params[key] = value
        
        # Update UI elements
        self.brightness_slider.value = self.adjustment_params['brightness']
        self.warmth_slider.value = self.adjustment_params['warmth']
        self.saturation_slider.value = self.adjustment_params['saturation']
        self.hue_slider.value = self.adjustment_params['hue_shift']
        
        self.brightness_value.text = str(self.adjustment_params['brightness'])
        self.warmth_value.text = str(self.adjustment_params['warmth'])
        self.saturation_value.text = str(self.adjustment_params['saturation'])
        self.hue_value.text = str(self.adjustment_params['hue_shift'])