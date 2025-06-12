import React, { useState } from 'react';
import { Upload, Palette, Sparkles, Camera } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import ImageUpload from '@/components/ImageUpload';
import SkinToneAnalysis from '@/components/SkinToneAnalysis';
import ColorRecommendations from '@/components/ColorRecommendations';
import SkinToneAdjuster from '@/components/SkinToneAdjuster';

const Index = () => {
  const [uploadedImage, setUploadedImage] = useState<string | null>(null);
  const [analyzedSkinTone, setAnalyzedSkinTone] = useState<string | null>(null);
  const [showAnalysis, setShowAnalysis] = useState(false);

  console.log('Index component rendered', { uploadedImage, analyzedSkinTone, showAnalysis });

  const handleImageUpload = (imageUrl: string) => {
    console.log('Image uploaded:', imageUrl);
    setUploadedImage(imageUrl);
    setShowAnalysis(true);
    // Simulate skin tone analysis
    setTimeout(() => {
      const skinTones = ['fair', 'light', 'medium', 'tan', 'deep'];
      const randomTone = skinTones[Math.floor(Math.random() * skinTones.length)];
      console.log('Analyzed skin tone:', randomTone);
      setAnalyzedSkinTone(randomTone);
    }, 1500);
  };

  const handleSkinToneChange = (newTone: string) => {
    console.log('Skin tone changed to:', newTone);
    setAnalyzedSkinTone(newTone);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-pink-50 to-blue-50">
      {/* Header */}
      <header className="relative overflow-hidden bg-gradient-beauty py-16 px-4">
        <div className="absolute inset-0 bg-black/10"></div>
        <div className="relative max-w-6xl mx-auto text-center">
          <div className="inline-flex items-center gap-2 mb-4 px-4 py-2 bg-white/20 rounded-full backdrop-blur-sm">
            <Sparkles className="w-5 h-5 text-white" />
            <span className="text-white font-medium">AI-Powered Color Analysis</span>
          </div>
          <h1 className="text-5xl md:text-7xl font-bold text-white mb-6 animate-fade-in">
            Color Harmony
          </h1>
          <p className="text-xl md:text-2xl text-white/90 mb-8 max-w-3xl mx-auto leading-relaxed">
            Discover your perfect color palette with AI-powered skin tone analysis. 
            Upload your photo and unlock colors that make you shine.
          </p>
          <div className="flex flex-wrap justify-center gap-4">
            <div className="flex items-center gap-2 text-white/80">
              <Camera className="w-5 h-5" />
              <span>Upload Photo</span>
            </div>
            <div className="flex items-center gap-2 text-white/80">
              <Palette className="w-5 h-5" />
              <span>Get Color Palette</span>
            </div>
            <div className="flex items-center gap-2 text-white/80">
              <Sparkles className="w-5 h-5" />
              <span>Adjust Skin Tone</span>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-6xl mx-auto px-4 py-12">
        {!uploadedImage ? (
          <div className="animate-fade-in">
            <ImageUpload onImageUpload={handleImageUpload} />
          </div>
        ) : (
          <div className="space-y-8 animate-fade-in">
            {/* Image Display */}
            <Card className="p-6 bg-white/80 backdrop-blur-sm border-white/30">
              <h2 className="text-2xl font-bold mb-4 text-gray-800">Your Photo</h2>
              <div className="flex flex-col lg:flex-row gap-8">
                <div className="flex-1">
                  <img 
                    src={uploadedImage} 
                    alt="Uploaded" 
                    className="w-full max-w-md mx-auto rounded-2xl shadow-2xl"
                  />
                </div>
                <div className="flex-1 space-y-6">
                  <Button 
                    onClick={() => {
                      setUploadedImage(null);
                      setAnalyzedSkinTone(null);
                      setShowAnalysis(false);
                    }}
                    variant="outline"
                    className="w-full"
                  >
                    <Upload className="w-4 h-4 mr-2" />
                    Upload New Photo
                  </Button>
                  
                  {analyzedSkinTone && (
                    <SkinToneAdjuster 
                      currentTone={analyzedSkinTone}
                      onToneChange={handleSkinToneChange}
                    />
                  )}
                </div>
              </div>
            </Card>

            {/* Analysis Results */}
            {showAnalysis && (
              <div className="grid lg:grid-cols-2 gap-8">
                <SkinToneAnalysis 
                  skinTone={analyzedSkinTone}
                  isLoading={!analyzedSkinTone}
                />
                <ColorRecommendations 
                  skinTone={analyzedSkinTone}
                  isLoading={!analyzedSkinTone}
                />
              </div>
            )}
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12 px-4 mt-20">
        <div className="max-w-6xl mx-auto text-center">
          <h3 className="text-2xl font-bold mb-4">Color Harmony</h3>
          <p className="text-gray-400 mb-6">
            Empowering your style with AI-powered color analysis
          </p>
          <div className="flex justify-center space-x-6 text-sm text-gray-500">
            <span>© 2024 Color Harmony</span>
            <span>•</span>
            <span>Powered by AI</span>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Index;