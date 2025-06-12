import React from 'react';
import { Palette, RefreshCw } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';

interface SkinToneAdjusterProps {
  currentTone: string;
  onToneChange: (tone: string) => void;
}

const skinToneOptions = [
  { id: 'fair', name: 'Fair', color: '#F5DEB3', description: 'Light with cool undertones' },
  { id: 'light', name: 'Light', color: '#DEB887', description: 'Light with warm undertones' },
  { id: 'medium', name: 'Medium', color: '#CD853F', description: 'Medium with olive undertones' },
  { id: 'tan', name: 'Tan', color: '#A0522D', description: 'Medium-dark with warm undertones' },
  { id: 'deep', name: 'Deep', color: '#8B4513', description: 'Deep with rich undertones' }
];

const SkinToneAdjuster: React.FC<SkinToneAdjusterProps> = ({ currentTone, onToneChange }) => {
  console.log('SkinToneAdjuster rendered', { currentTone });

  return (
    <Card className="p-4 bg-white/60 backdrop-blur-sm border-white/30">
      <div className="flex items-center gap-2 mb-4">
        <RefreshCw className="w-4 h-4 text-gray-600" />
        <h4 className="font-semibold text-gray-800">Adjust Skin Tone</h4>
      </div>
      
      <p className="text-sm text-gray-600 mb-4">
        Not quite right? Select your actual skin tone for better color recommendations.
      </p>
      
      <div className="space-y-2">
        {skinToneOptions.map((tone) => (
          <Button
            key={tone.id}
            variant={currentTone === tone.id ? "default" : "outline"}
            size="sm"
            onClick={() => {
              console.log('Skin tone button clicked:', tone.id);
              onToneChange(tone.id);
            }}
            className={`w-full justify-start gap-3 ${
              currentTone === tone.id 
                ? 'bg-gradient-to-r from-primary to-purple-600 text-white' 
                : 'hover:bg-gray-50'
            }`}
          >
            <div 
              className="w-4 h-4 rounded-full border border-white/50"
              style={{ backgroundColor: tone.color }}
            ></div>
            <div className="text-left">
              <div className="font-medium">{tone.name}</div>
              <div className="text-xs opacity-75">{tone.description}</div>
            </div>
          </Button>
        ))}
      </div>
      
      <div className="mt-4 p-3 bg-blue-50 rounded-lg border border-blue-100">
        <p className="text-xs text-blue-700">
          <Palette className="w-3 h-3 inline mr-1" />
          Color recommendations will update automatically when you change your skin tone.
        </p>
      </div>
    </Card>
  );
};

export default SkinToneAdjuster;