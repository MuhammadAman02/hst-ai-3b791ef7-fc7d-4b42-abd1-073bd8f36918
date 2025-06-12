import React from 'react';
import { Palette, Heart, Star } from 'lucide-react';
import { Card } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';

interface ColorRecommendationsProps {
  skinTone: string | null;
  isLoading: boolean;
}

const colorRecommendations = {
  fair: {
    best: [
      { name: 'Soft Pink', color: '#F8BBD9', category: 'Pastels' },
      { name: 'Lavender', color: '#E6E6FA', category: 'Cool' },
      { name: 'Mint Green', color: '#98FB98', category: 'Cool' },
      { name: 'Baby Blue', color: '#87CEEB', category: 'Cool' },
      { name: 'Cream', color: '#F5F5DC', category: 'Neutral' },
      { name: 'Light Gray', color: '#D3D3D3', category: 'Neutral' }
    ],
    avoid: [
      { name: 'Bright Orange', color: '#FF4500', reason: 'Too harsh' },
      { name: 'Neon Yellow', color: '#FFFF00', reason: 'Overwhelming' },
      { name: 'Hot Pink', color: '#FF1493', reason: 'Too bold' }
    ]
  },
  light: {
    best: [
      { name: 'Coral', color: '#FF7F50', category: 'Warm' },
      { name: 'Peach', color: '#FFCBA4', category: 'Warm' },
      { name: 'Golden Yellow', color: '#FFD700', category: 'Warm' },
      { name: 'Warm Beige', color: '#F5F5DC', category: 'Neutral' },
      { name: 'Turquoise', color: '#40E0D0', category: 'Cool' },
      { name: 'Soft Brown', color: '#DEB887', category: 'Earth' }
    ],
    avoid: [
      { name: 'Icy Blue', color: '#B0E0E6', reason: 'Too cool' },
      { name: 'Pure White', color: '#FFFFFF', reason: 'Washes out' },
      { name: 'Black', color: '#000000', reason: 'Too harsh' }
    ]
  },
  medium: {
    best: [
      { name: 'Emerald Green', color: '#50C878', category: 'Rich' },
      { name: 'Deep Purple', color: '#663399', category: 'Rich' },
      { name: 'Burnt Orange', color: '#CC5500', category: 'Warm' },
      { name: 'Olive Green', color: '#808000', category: 'Earth' },
      { name: 'Burgundy', color: '#800020', category: 'Rich' },
      { name: 'Teal', color: '#008080', category: 'Cool' }
    ],
    avoid: [
      { name: 'Pale Pink', color: '#FFB6C1', reason: 'Too light' },
      { name: 'Light Yellow', color: '#FFFFE0', reason: 'Washes out' },
      { name: 'Gray', color: '#808080', reason: 'Dull' }
    ]
  },
  tan: {
    best: [
      { name: 'Rich Gold', color: '#FFD700', category: 'Warm' },
      { name: 'Deep Red', color: '#8B0000', category: 'Rich' },
      { name: 'Forest Green', color: '#228B22', category: 'Earth' },
      { name: 'Royal Blue', color: '#4169E1', category: 'Cool' },
      { name: 'Chocolate Brown', color: '#7B3F00', category: 'Earth' },
      { name: 'Amber', color: '#FFBF00', category: 'Warm' }
    ],
    avoid: [
      { name: 'Pastel Pink', color: '#FFB6C1', reason: 'Too soft' },
      { name: 'Light Blue', color: '#ADD8E6', reason: 'Lacks contrast' },
      { name: 'Beige', color: '#F5F5DC', reason: 'Too similar' }
    ]
  },
  deep: {
    best: [
      { name: 'Bright White', color: '#FFFFFF', category: 'Contrast' },
      { name: 'Electric Blue', color: '#0080FF', category: 'Bold' },
      { name: 'Fuchsia', color: '#FF00FF', category: 'Bold' },
      { name: 'Lime Green', color: '#32CD32', category: 'Bold' },
      { name: 'Golden Yellow', color: '#FFD700', category: 'Warm' },
      { name: 'Deep Purple', color: '#4B0082', category: 'Rich' }
    ],
    avoid: [
      { name: 'Brown', color: '#A52A2A', reason: 'Too similar' },
      { name: 'Olive', color: '#808000', reason: 'Muddy' },
      { name: 'Muted Colors', color: '#696969', reason: 'Lack vibrancy' }
    ]
  }
};

const ColorRecommendations: React.FC<ColorRecommendationsProps> = ({ skinTone, isLoading }) => {
  console.log('ColorRecommendations rendered', { skinTone, isLoading });

  if (isLoading) {
    return (
      <Card className="p-6 skin-tone-card">
        <div className="flex items-center gap-3 mb-6">
          <div className="w-8 h-8 bg-gradient-to-r from-primary to-purple-600 rounded-full flex items-center justify-center animate-pulse">
            <Palette className="w-4 h-4 text-white" />
          </div>
          <h3 className="text-xl font-bold text-gray-800">Generating Color Palette...</h3>
        </div>
        
        <div className="space-y-4">
          <div className="grid grid-cols-3 gap-3">
            {[...Array(6)].map((_, i) => (
              <div key={i} className="h-16 bg-gray-200 rounded-lg animate-pulse"></div>
            ))}
          </div>
        </div>
      </Card>
    );
  }

  if (!skinTone || !colorRecommendations[skinTone as keyof typeof colorRecommendations]) {
    return (
      <Card className="p-6 skin-tone-card">
        <div className="text-center text-gray-500">
          <Palette className="w-12 h-12 mx-auto mb-4 opacity-50" />
          <p>Unable to generate color recommendations</p>
        </div>
      </Card>
    );
  }

  const recommendations = colorRecommendations[skinTone as keyof typeof colorRecommendations];

  return (
    <Card className="p-6 skin-tone-card animate-fade-in">
      <div className="flex items-center gap-3 mb-6">
        <div className="w-8 h-8 bg-gradient-to-r from-primary to-purple-600 rounded-full flex items-center justify-center">
          <Heart className="w-4 h-4 text-white" />
        </div>
        <h3 className="text-xl font-bold text-gray-800">Perfect Colors for You</h3>
      </div>
      
      <div className="space-y-6">
        {/* Best Colors */}
        <div>
          <div className="flex items-center gap-2 mb-4">
            <Star className="w-5 h-5 text-yellow-500" />
            <h4 className="font-semibold text-gray-800">Colors that make you shine</h4>
          </div>
          
          <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 mb-4">
            {recommendations.best.map((color, index) => (
              <div key={index} className="group cursor-pointer">
                <div 
                  className="color-swatch mx-auto mb-2"
                  style={{ backgroundColor: color.color }}
                  title={color.name}
                ></div>
                <div className="text-center">
                  <p className="text-xs font-medium text-gray-800">{color.name}</p>
                  <Badge variant="outline" className="text-xs mt-1">
                    {color.category}
                  </Badge>
                </div>
              </div>
            ))}
          </div>
        </div>
        
        {/* Colors to Avoid */}
        <div className="border-t pt-6">
          <h4 className="font-semibold text-gray-800 mb-4">Colors to use sparingly</h4>
          
          <div className="space-y-3">
            {recommendations.avoid.map((color, index) => (
              <div key={index} className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg">
                <div 
                  className="w-8 h-8 rounded-full border-2 border-gray-300"
                  style={{ backgroundColor: color.color }}
                ></div>
                <div className="flex-1">
                  <p className="text-sm font-medium text-gray-800">{color.name}</p>
                  <p className="text-xs text-gray-600">{color.reason}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
        
        <div className="bg-gradient-to-r from-purple-50 to-pink-50 p-4 rounded-xl border border-purple-100">
          <p className="text-sm text-gray-700">
            💡 <strong>Pro tip:</strong> These colors will enhance your natural beauty and make your skin glow. 
            Try incorporating them into your wardrobe, makeup, or accessories!
          </p>
        </div>
      </div>
    </Card>
  );
};

export default ColorRecommendations;