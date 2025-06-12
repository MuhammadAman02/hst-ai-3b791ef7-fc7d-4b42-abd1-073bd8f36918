import React from 'react';
import { Palette, Sparkles, Eye } from 'lucide-react';
import { Card } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';

interface SkinToneAnalysisProps {
  skinTone: string | null;
  isLoading: boolean;
}

const skinToneData = {
  fair: {
    name: 'Fair',
    description: 'Light complexion with cool or neutral undertones',
    undertone: 'Cool/Neutral',
    characteristics: ['Burns easily in sun', 'Often has pink or red undertones', 'May have freckles'],
    color: '#F5DEB3',
    gradient: 'from-pink-100 to-rose-100'
  },
  light: {
    name: 'Light',
    description: 'Light to medium complexion with warm undertones',
    undertone: 'Warm',
    characteristics: ['Tans gradually', 'Golden or yellow undertones', 'Even skin tone'],
    color: '#DEB887',
    gradient: 'from-yellow-100 to-orange-100'
  },
  medium: {
    name: 'Medium',
    description: 'Medium complexion with warm or olive undertones',
    undertone: 'Warm/Olive',
    characteristics: ['Tans well', 'Olive or golden undertones', 'Rich skin tone'],
    color: '#CD853F',
    gradient: 'from-amber-100 to-yellow-100'
  },
  tan: {
    name: 'Tan',
    description: 'Medium to dark complexion with warm undertones',
    undertone: 'Warm',
    characteristics: ['Rarely burns', 'Golden or bronze undertones', 'Natural glow'],
    color: '#A0522D',
    gradient: 'from-orange-100 to-amber-100'
  },
  deep: {
    name: 'Deep',
    description: 'Deep complexion with rich undertones',
    undertone: 'Rich/Warm',
    characteristics: ['Never burns', 'Rich golden or red undertones', 'Beautiful natural depth'],
    color: '#8B4513',
    gradient: 'from-amber-100 to-orange-100'
  }
};

const SkinToneAnalysis: React.FC<SkinToneAnalysisProps> = ({ skinTone, isLoading }) => {
  console.log('SkinToneAnalysis rendered', { skinTone, isLoading });

  if (isLoading) {
    return (
      <Card className="p-6 skin-tone-card">
        <div className="flex items-center gap-3 mb-6">
          <div className="w-8 h-8 bg-gradient-to-r from-primary to-purple-600 rounded-full flex items-center justify-center animate-pulse">
            <Eye className="w-4 h-4 text-white" />
          </div>
          <h3 className="text-xl font-bold text-gray-800">Analyzing Skin Tone...</h3>
        </div>
        
        <div className="space-y-4">
          <div className="h-4 bg-gray-200 rounded animate-pulse"></div>
          <div className="h-4 bg-gray-200 rounded animate-pulse w-3/4"></div>
          <div className="h-4 bg-gray-200 rounded animate-pulse w-1/2"></div>
        </div>
        
        <div className="mt-6 flex justify-center">
          <div className="w-16 h-16 bg-gray-200 rounded-full animate-pulse"></div>
        </div>
      </Card>
    );
  }

  if (!skinTone || !skinToneData[skinTone as keyof typeof skinToneData]) {
    return (
      <Card className="p-6 skin-tone-card">
        <div className="text-center text-gray-500">
          <Palette className="w-12 h-12 mx-auto mb-4 opacity-50" />
          <p>Unable to analyze skin tone</p>
        </div>
      </Card>
    );
  }

  const toneData = skinToneData[skinTone as keyof typeof skinToneData];

  return (
    <Card className="p-6 skin-tone-card animate-fade-in">
      <div className="flex items-center gap-3 mb-6">
        <div className="w-8 h-8 bg-gradient-to-r from-primary to-purple-600 rounded-full flex items-center justify-center">
          <Sparkles className="w-4 h-4 text-white" />
        </div>
        <h3 className="text-xl font-bold text-gray-800">Skin Tone Analysis</h3>
      </div>
      
      <div className="space-y-6">
        <div className="flex items-center gap-4">
          <div 
            className="w-16 h-16 rounded-full border-4 border-white shadow-lg"
            style={{ backgroundColor: toneData.color }}
          ></div>
          <div>
            <h4 className="text-2xl font-bold text-gray-800">{toneData.name}</h4>
            <p className="text-gray-600">{toneData.description}</p>
          </div>
        </div>
        
        <div className="space-y-3">
          <div className="flex items-center gap-2">
            <Badge variant="secondary" className="bg-gradient-to-r from-purple-100 to-pink-100">
              Undertone: {toneData.undertone}
            </Badge>
          </div>
          
          <div>
            <h5 className="font-semibold text-gray-800 mb-2">Characteristics:</h5>
            <ul className="space-y-1">
              {toneData.characteristics.map((char, index) => (
                <li key={index} className="flex items-center gap-2 text-gray-600">
                  <div className="w-1.5 h-1.5 bg-primary rounded-full"></div>
                  {char}
                </li>
              ))}
            </ul>
          </div>
        </div>
        
        <div className={`p-4 rounded-xl bg-gradient-to-r ${toneData.gradient} border border-white/50`}>
          <p className="text-sm text-gray-700 font-medium">
            ✨ Your {toneData.name.toLowerCase()} skin tone has beautiful {toneData.undertone.toLowerCase()} undertones 
            that will look stunning with the right color palette!
          </p>
        </div>
      </div>
    </Card>
  );
};

export default SkinToneAnalysis;