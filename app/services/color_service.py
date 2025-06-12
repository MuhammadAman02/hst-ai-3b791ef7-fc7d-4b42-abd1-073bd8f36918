import cv2
import numpy as np
from sklearn.cluster import KMeans
from scipy.spatial.distance import euclidean
import webcolors
from typing import Dict, List, Any, Tuple, Optional
import asyncio

class ColorService:
    """Service for color analysis and skin tone detection."""
    
    def __init__(self):
        # Define skin tone reference colors (RGB)
        self.skin_tone_references = {
            'very_light': (255, 219, 172),
            'light': (241, 194, 125),
            'light_medium': (224, 172, 105),
            'medium': (198, 134, 66),
            'medium_dark': (161, 102, 94),
            'dark': (110, 84, 61),
            'very_dark': (54, 34, 26)
        }
        
        # Color harmony rules
        self.color_harmonies = {
            'warm': {
                'best_colors': [
                    '#D2691E', '#CD853F', '#DEB887', '#F4A460', '#DAA520',
                    '#B8860B', '#FF6347', '#FF7F50', '#FFA07A', '#FA8072',
                    '#E9967A', '#F0E68C', '#BDB76B', '#9ACD32', '#6B8E23'
                ],
                'avoid_colors': [
                    '#4169E1', '#0000FF', '#1E90FF', '#00BFFF', '#87CEEB',
                    '#B0C4DE', '#778899', '#2F4F4F', '#008B8B', '#20B2AA'
                ]
            },
            'cool': {
                'best_colors': [
                    '#4169E1', '#0000FF', '#1E90FF', '#00BFFF', '#87CEEB',
                    '#B0C4DE', '#6495ED', '#7B68EE', '#9370DB', '#8A2BE2',
                    '#9400D3', '#4B0082', '#483D8B', '#2E8B57', '#008B8B'
                ],
                'avoid_colors': [
                    '#FF6347', '#FF7F50', '#FFA07A', '#FA8072', '#E9967A',
                    '#D2691E', '#CD853F', '#DEB887', '#F4A460', '#DAA520'
                ]
            },
            'neutral': {
                'best_colors': [
                    '#708090', '#2F4F4F', '#696969', '#778899', '#B0C4DE',
                    '#D3D3D3', '#A9A9A9', '#C0C0C0', '#DCDCDC', '#F5F5F5',
                    '#8FBC8F', '#20B2AA', '#48D1CC', '#40E0D0', '#00CED1'
                ],
                'avoid_colors': []  # Neutral can wear most colors
            }
        }
        
        # Seasonal color palettes
        self.seasonal_palettes = {
            'Spring': ['#FFB6C1', '#FF69B4', '#FF1493', '#DC143C', '#B22222',
                      '#FF6347', '#FF4500', '#FFA500', '#FFD700', '#ADFF2F'],
            'Summer': ['#E6E6FA', '#D8BFD8', '#DDA0DD', '#BA55D3', '#9370DB',
                      '#6495ED', '#4682B4', '#5F9EA0', '#48D1CC', '#40E0D0'],
            'Autumn': ['#8B4513', '#A0522D', '#CD853F', '#D2691E', '#FF8C00',
                      '#FF6347', '#DC143C', '#B22222', '#8B0000', '#556B2F'],
            'Winter': ['#000000', '#2F4F4F', '#191970', '#000080', '#4B0082',
                      '#8B008B', '#FF1493', '#DC143C', '#B22222', '#8B0000']
        }
    
    async def analyze_skin_tone(self, image: np.ndarray) -> Dict[str, Any]:
        """Analyze skin tone from an image."""
        try:
            # Extract skin pixels
            skin_pixels = await self._extract_skin_pixels(image)
            
            if len(skin_pixels) == 0:
                raise ValueError("No skin pixels detected in image")
            
            # Get dominant skin color
            dominant_color = await self._get_dominant_color(skin_pixels)
            
            # Classify skin tone
            skin_tone_category = await self._classify_skin_tone(dominant_color)
            
            # Determine undertone
            undertone = await self._determine_undertone(skin_pixels)
            
            # Calculate confidence score
            confidence = await self._calculate_confidence(skin_pixels, dominant_color)
            
            return {
                'primary_color': self._rgb_to_hex(dominant_color),
                'category': skin_tone_category,
                'undertone': undertone,
                'confidence': confidence,
                'rgb_values': dominant_color.tolist(),
                'analysis_metadata': {
                    'pixels_analyzed': len(skin_pixels),
                    'color_variance': np.std(skin_pixels, axis=0).tolist()
                }
            }
            
        except Exception as e:
            raise Exception(f"Error analyzing skin tone: {str(e)}")
    
    async def _extract_skin_pixels(self, image: np.ndarray) -> np.ndarray:
        """Extract skin-colored pixels from an image."""
        # Convert RGB to YCrCb color space (better for skin detection)
        ycrcb = cv2.cvtColor(image, cv2.COLOR_RGB2YCrCb)
        
        # Define skin color range in YCrCb
        lower_skin = np.array([0, 133, 77], dtype=np.uint8)
        upper_skin = np.array([255, 173, 127], dtype=np.uint8)
        
        # Create mask for skin pixels
        skin_mask = cv2.inRange(ycrcb, lower_skin, upper_skin)
        
        # Apply morphological operations to clean up the mask
        kernel = np.ones((3, 3), np.uint8)
        skin_mask = cv2.morphologyEx(skin_mask, cv2.MORPH_OPEN, kernel)
        skin_mask = cv2.morphologyEx(skin_mask, cv2.MORPH_CLOSE, kernel)
        
        # Extract skin pixels
        skin_pixels = image[skin_mask > 0]
        
        # Additional filtering based on RGB values
        if len(skin_pixels) > 0:
            # Remove pixels that are too dark or too light
            brightness = np.mean(skin_pixels, axis=1)
            valid_brightness = (brightness > 50) & (brightness < 220)
            skin_pixels = skin_pixels[valid_brightness]
            
            # Remove pixels with unusual color ratios
            if len(skin_pixels) > 0:
                r, g, b = skin_pixels[:, 0], skin_pixels[:, 1], skin_pixels[:, 2]
                # Skin typically has R > G > B
                valid_ratios = (r >= g * 0.8) & (g >= b * 0.8)
                skin_pixels = skin_pixels[valid_ratios]
        
        return skin_pixels
    
    async def _get_dominant_color(self, pixels: np.ndarray, n_colors: int = 5) -> np.ndarray:
        """Get the dominant color from a set of pixels using K-means clustering."""
        if len(pixels) < n_colors:
            return np.mean(pixels, axis=0).astype(int)
        
        # Perform K-means clustering
        kmeans = KMeans(n_clusters=n_colors, random_state=42, n_init=10)
        kmeans.fit(pixels)
        
        # Get cluster centers and labels
        colors = kmeans.cluster_centers_
        labels = kmeans.labels_
        
        # Find the most common cluster (dominant color)
        label_counts = np.bincount(labels)
        dominant_color_index = np.argmax(label_counts)
        
        return colors[dominant_color_index].astype(int)
    
    async def _classify_skin_tone(self, color: np.ndarray) -> str:
        """Classify skin tone based on color values."""
        min_distance = float('inf')
        closest_tone = 'medium'
        
        for tone_name, reference_color in self.skin_tone_references.items():
            distance = euclidean(color, reference_color)
            if distance < min_distance:
                min_distance = distance
                closest_tone = tone_name
        
        # Convert internal names to user-friendly names
        tone_mapping = {
            'very_light': 'Very Light',
            'light': 'Light',
            'light_medium': 'Light-Medium',
            'medium': 'Medium',
            'medium_dark': 'Medium-Dark',
            'dark': 'Dark',
            'very_dark': 'Very Dark'
        }
        
        return tone_mapping.get(closest_tone, 'Medium')
    
    async def _determine_undertone(self, skin_pixels: np.ndarray) -> str:
        """Determine skin undertone (warm, cool, or neutral)."""
        if len(skin_pixels) == 0:
            return 'neutral'
        
        # Calculate average color values
        avg_color = np.mean(skin_pixels, axis=0)
        r, g, b = avg_color
        
        # Calculate color ratios and differences
        red_yellow_ratio = (r + g) / (b + 1)  # Warm indicator
        blue_pink_ratio = (b + r) / (g + 1)   # Cool indicator
        
        # Determine undertone based on ratios
        if red_yellow_ratio > 2.2:
            return 'warm'
        elif blue_pink_ratio > 2.0:
            return 'cool'
        else:
            return 'neutral'
    
    async def _calculate_confidence(self, skin_pixels: np.ndarray, dominant_color: np.ndarray) -> float:
        """Calculate confidence score for the skin tone analysis."""
        if len(skin_pixels) == 0:
            return 0.0
        
        # Calculate how consistent the skin pixels are
        distances = [euclidean(pixel, dominant_color) for pixel in skin_pixels]
        avg_distance = np.mean(distances)
        
        # Convert distance to confidence (lower distance = higher confidence)
        max_expected_distance = 50  # Empirically determined
        confidence = max(0.0, 1.0 - (avg_distance / max_expected_distance))
        
        # Boost confidence if we have many skin pixels
        pixel_count_factor = min(1.0, len(skin_pixels) / 1000)
        confidence = confidence * (0.7 + 0.3 * pixel_count_factor)
        
        return min(1.0, confidence)
    
    async def get_color_recommendations(self, skin_tone_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate color recommendations based on skin tone analysis."""
        try:
            undertone = skin_tone_data.get('undertone', 'neutral')
            category = skin_tone_data.get('category', 'Medium')
            
            # Get base color recommendations
            harmony_colors = self.color_harmonies.get(undertone, self.color_harmonies['neutral'])
            
            # Process best colors
            best_colors = []
            for color_hex in harmony_colors['best_colors'][:12]:  # Limit to 12 colors
                color_info = await self._get_color_info(color_hex, undertone)
                best_colors.append(color_info)
            
            # Process colors to avoid
            avoid_colors = []
            for color_hex in harmony_colors['avoid_colors'][:8]:  # Limit to 8 colors
                color_info = await self._get_color_info(color_hex, undertone, is_avoid=True)
                avoid_colors.append(color_info)
            
            # Determine seasonal palette
            seasonal_palette = await self._get_seasonal_palette(undertone, category)
            
            # Generate outfit suggestions
            outfit_suggestions = await self._generate_outfit_suggestions(undertone, best_colors)
            
            return {
                'best_colors': best_colors,
                'avoid_colors': avoid_colors,
                'seasonal_palette': seasonal_palette,
                'outfit_suggestions': outfit_suggestions,
                'undertone': undertone,
                'category': category
            }
            
        except Exception as e:
            raise Exception(f"Error generating color recommendations: {str(e)}")
    
    async def _get_color_info(self, color_hex: str, undertone: str, is_avoid: bool = False) -> Dict[str, Any]:
        """Get detailed information about a color."""
        try:
            # Get color name
            color_name = await self._get_color_name(color_hex)
            
            # Calculate confidence based on undertone match
            confidence = await self._calculate_color_confidence(color_hex, undertone, is_avoid)
            
            # Get usage suggestions
            usage = await self._get_color_usage_suggestions(color_hex, undertone, is_avoid)
            
            return {
                'hex': color_hex,
                'name': color_name,
                'confidence': confidence,
                'usage': usage,
                'undertone_match': undertone
            }
            
        except Exception as e:
            return {
                'hex': color_hex,
                'name': 'Unknown Color',
                'confidence': 0.5,
                'usage': 'General use',
                'undertone_match': undertone
            }
    
    async def _get_color_name(self, color_hex: str) -> str:
        """Get the name of a color from its hex value."""
        try:
            # Convert hex to RGB
            rgb = tuple(int(color_hex[i:i+2], 16) for i in (1, 3, 5))
            
            # Try to get exact match
            try:
                return webcolors.rgb_to_name(rgb)
            except ValueError:
                # Find closest named color
                min_colors = {}
                for key, name in webcolors.CSS3_HEX_TO_NAMES.items():
                    r_c, g_c, b_c = webcolors.hex_to_rgb(key)
                    rd = (r_c - rgb[0]) ** 2
                    gd = (g_c - rgb[1]) ** 2
                    bd = (b_c - rgb[2]) ** 2
                    min_colors[(rd + gd + bd)] = name
                
                return min_colors[min(min_colors.keys())]
                
        except Exception:
            return "Custom Color"
    
    async def _calculate_color_confidence(self, color_hex: str, undertone: str, is_avoid: bool) -> float:
        """Calculate confidence score for a color recommendation."""
        if is_avoid:
            return 0.8  # High confidence for colors to avoid
        
        # Base confidence varies by undertone
        base_confidence = {
            'warm': 0.85,
            'cool': 0.85,
            'neutral': 0.75  # Neutral has more flexibility
        }.get(undertone, 0.7)
        
        # Add some randomness for variety
        import random
        variation = random.uniform(-0.1, 0.1)
        
        return max(0.5, min(1.0, base_confidence + variation))
    
    async def _get_color_usage_suggestions(self, color_hex: str, undertone: str, is_avoid: bool) -> str:
        """Get usage suggestions for a color."""
        if is_avoid:
            return "Use sparingly as accents or in small doses"
        
        # Convert hex to RGB for analysis
        rgb = tuple(int(color_hex[i:i+2], 16) for i in (1, 3, 5))
        brightness = sum(rgb) / 3
        
        if brightness > 200:
            return "Perfect for tops, dresses, and statement pieces"
        elif brightness > 100:
            return "Great for blouses, accessories, and casual wear"
        else:
            return "Excellent for formal wear, outerwear, and evening attire"
    
    async def _get_seasonal_palette(self, undertone: str, category: str) -> Dict[str, Any]:
        """Determine seasonal color palette."""
        # Map undertone to season
        season_mapping = {
            'warm': 'Autumn' if 'dark' in category.lower() else 'Spring',
            'cool': 'Winter' if 'dark' in category.lower() else 'Summer',
            'neutral': 'Summer'  # Default for neutral
        }
        
        season = season_mapping.get(undertone, 'Summer')
        colors = self.seasonal_palettes.get(season, self.seasonal_palettes['Summer'])
        
        return {
            'season': season,
            'colors': colors,
            'description': f'Your {season.lower()} palette complements your {undertone} undertones beautifully'
        }
    
    async def _generate_outfit_suggestions(self, undertone: str, best_colors: List[Dict]) -> List[Dict[str, Any]]:
        """Generate outfit color combination suggestions."""
        if len(best_colors) < 3:
            return []
        
        suggestions = []
        
        # Create complementary combinations
        for i in range(min(3, len(best_colors) - 2)):
            primary_color = best_colors[i]
            secondary_color = best_colors[i + 1]
            accent_color = best_colors[i + 2]
            
            suggestion = {
                'name': f'Elegant {primary_color["name"]} Combination',
                'colors': [primary_color['hex'], secondary_color['hex'], accent_color['hex']],
                'description': f'Pair {primary_color["name"].lower()} with {secondary_color["name"].lower()} and {accent_color["name"].lower()} accents',
                'occasion': 'Professional' if i == 0 else 'Casual' if i == 1 else 'Evening'
            }
            suggestions.append(suggestion)
        
        return suggestions
    
    def _rgb_to_hex(self, rgb: np.ndarray) -> str:
        """Convert RGB values to hex color code."""
        return '#{:02x}{:02x}{:02x}'.format(int(rgb[0]), int(rgb[1]), int(rgb[2]))
    
    def _hex_to_rgb(self, hex_color: str) -> Tuple[int, int, int]:
        """Convert hex color code to RGB values."""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))