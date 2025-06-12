import React, { useRef, useState } from 'react';
import { Upload, Camera, Image as ImageIcon } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';

interface ImageUploadProps {
  onImageUpload: (imageUrl: string) => void;
}

const ImageUpload: React.FC<ImageUploadProps> = ({ onImageUpload }) => {
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [isDragging, setIsDragging] = useState(false);
  const [isUploading, setIsUploading] = useState(false);

  console.log('ImageUpload component rendered', { isDragging, isUploading });

  const handleFileSelect = (file: File) => {
    console.log('File selected:', file.name, file.type, file.size);
    
    if (!file.type.startsWith('image/')) {
      console.error('Invalid file type:', file.type);
      return;
    }

    setIsUploading(true);
    const reader = new FileReader();
    
    reader.onload = (e) => {
      const result = e.target?.result as string;
      console.log('File read successfully, length:', result.length);
      setTimeout(() => {
        onImageUpload(result);
        setIsUploading(false);
      }, 1000);
    };
    
    reader.onerror = (error) => {
      console.error('Error reading file:', error);
      setIsUploading(false);
    };
    
    reader.readAsDataURL(file);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    
    const files = Array.from(e.dataTransfer.files);
    console.log('Files dropped:', files.length);
    
    if (files.length > 0) {
      handleFileSelect(files[0]);
    }
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleButtonClick = () => {
    console.log('Upload button clicked');
    fileInputRef.current?.click();
  };

  const handleFileInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    console.log('File input changed:', files?.length);
    
    if (files && files.length > 0) {
      handleFileSelect(files[0]);
    }
  };

  return (
    <div className="max-w-2xl mx-auto">
      <Card 
        className={`p-12 text-center transition-all duration-300 cursor-pointer ${
          isDragging 
            ? 'border-primary border-2 bg-primary/5 scale-105' 
            : 'border-dashed border-2 border-gray-300 hover:border-primary hover:bg-primary/5'
        } ${isUploading ? 'animate-pulse' : ''}`}
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onClick={handleButtonClick}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept="image/*"
          onChange={handleFileInputChange}
          className="hidden"
        />
        
        <div className="space-y-6">
          <div className="flex justify-center">
            {isUploading ? (
              <div className="w-16 h-16 border-4 border-primary border-t-transparent rounded-full animate-spin"></div>
            ) : (
              <div className="w-16 h-16 bg-gradient-to-br from-primary to-purple-600 rounded-full flex items-center justify-center animate-float">
                <Upload className="w-8 h-8 text-white" />
              </div>
            )}
          </div>
          
          <div>
            <h3 className="text-2xl font-bold text-gray-800 mb-2">
              {isUploading ? 'Processing your photo...' : 'Upload Your Photo'}
            </h3>
            <p className="text-gray-600 mb-6">
              {isUploading 
                ? 'Please wait while we prepare your image for analysis'
                : 'Drag and drop your photo here, or click to browse'
              }
            </p>
          </div>
          
          {!isUploading && (
            <>
              <Button 
                size="lg" 
                className="bg-gradient-to-r from-primary to-purple-600 hover:from-primary/90 hover:to-purple-600/90"
              >
                <Camera className="w-5 h-5 mr-2" />
                Choose Photo
              </Button>
              
              <div className="flex items-center justify-center space-x-8 text-sm text-gray-500 mt-8">
                <div className="flex items-center space-x-2">
                  <ImageIcon className="w-4 h-4" />
                  <span>JPG, PNG, WebP</span>
                </div>
                <div className="flex items-center space-x-2">
                  <Upload className="w-4 h-4" />
                  <span>Max 10MB</span>
                </div>
              </div>
            </>
          )}
        </div>
      </Card>
      
      <div className="mt-8 text-center text-sm text-gray-500">
        <p>Your photo is processed locally and never stored on our servers</p>
      </div>
    </div>
  );
};

export default ImageUpload;