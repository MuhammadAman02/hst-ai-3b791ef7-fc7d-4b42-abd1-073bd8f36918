# 🎨 Color Harmony - AI Skin Tone & Color Analysis

A sophisticated AI-powered application that analyzes skin tones and provides personalized color recommendations. Built with Python, NiceGUI, and advanced computer vision techniques.

## ✨ Features

### 🔍 **AI-Powered Skin Tone Analysis**
- Advanced computer vision using OpenCV and YCrCb color space
- Face detection for accurate skin tone extraction
- Undertone classification (warm, cool, neutral)
- Confidence scoring for analysis reliability

### 🎨 **Personalized Color Recommendations**
- Curated color palettes based on color harmony theory
- Seasonal color analysis (Spring, Summer, Autumn, Winter)
- Outfit color combination suggestions
- Colors to enhance vs. colors to avoid

### 🎛️ **Real-Time Skin Tone Adjustment**
- Interactive controls for brightness, warmth, saturation, and hue
- Preset adjustments for quick modifications
- Live preview of changes
- Re-analysis with adjusted skin tone

### 💎 **Professional UI/UX**
- Modern gradient design with glass-morphism effects
- Responsive layout for all devices
- Smooth animations and transitions
- Accessibility-compliant interface

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd color-harmony
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python main.py
   ```

4. **Open your browser**
   Navigate to `http://localhost:8000`

## 🏗️ Architecture

### **Technology Stack**
- **Frontend**: NiceGUI (Python-based web UI)
- **Backend**: Python with FastAPI integration
- **Computer Vision**: OpenCV, NumPy, scikit-learn
- **Image Processing**: Pillow, scipy
- **Configuration**: Pydantic Settings
- **Deployment**: Docker + Fly.io

### **Project Structure**
```
color-harmony/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── dockerfile             # Container configuration
├── fly.toml               # Deployment configuration
├── .env                   # Environment variables
├── app/
│   ├── main.py            # Main UI pages
│   ├── config.py          # Application configuration
│   ├── components/        # UI components
│   │   ├── image_upload.py
│   │   ├── skin_tone_analysis.py
│   │   ├── color_recommendations.py
│   │   └── skin_tone_adjuster.py
│   └── services/          # Business logic
│       ├── color_service.py
│       └── image_service.py
└── uploads/               # Uploaded images storage
```

## 🎯 How It Works

### **1. Image Upload**
- Drag-and-drop or click to upload
- Supports JPG, PNG, WebP formats
- Automatic file validation and resizing
- Secure file handling

### **2. Skin Tone Analysis**
- **Face Detection**: Locates facial regions for accurate analysis
- **Skin Pixel Extraction**: Uses YCrCb color space for skin detection
- **Color Clustering**: K-means algorithm finds dominant skin colors
- **Undertone Classification**: Analyzes color ratios to determine warm/cool/neutral

### **3. Color Recommendations**
- **Color Harmony Theory**: Applies professional color matching principles
- **Seasonal Analysis**: Maps skin tones to seasonal color palettes
- **Confidence Scoring**: Provides reliability metrics for each recommendation
- **Outfit Suggestions**: Creates harmonious color combinations

### **4. Skin Tone Adjustment**
- **Real-Time Processing**: Instant preview of adjustments
- **Multiple Parameters**: Brightness, warmth, saturation, hue shift
- **Preset Options**: Quick adjustments for common preferences
- **Re-Analysis**: Updates recommendations based on adjusted skin tone

## 🔧 Configuration

### **Environment Variables**
```bash
# Application Settings
APP_NAME=Color Harmony - AI Skin Tone Analysis
DEBUG=false

# Server Settings
HOST=0.0.0.0
PORT=8000

# File Upload Settings
MAX_FILE_SIZE=10485760
ALLOWED_EXTENSIONS=.jpg,.jpeg,.png,.webp

# Image Processing Settings
MAX_IMAGE_WIDTH=1920
MAX_IMAGE_HEIGHT=1080
CONFIDENCE_THRESHOLD=0.7
```

## 🐳 Docker Deployment

### **Build and Run**
```bash
# Build the image
docker build -t color-harmony .

# Run the container
docker run -p 8000:8000 color-harmony
```

### **Fly.io Deployment**
```bash
# Install Fly CLI
curl -L https://fly.io/install.sh | sh

# Deploy to Fly.io
fly deploy
```

## 🧪 API Endpoints

### **Health Check**
```
GET /health
```
Returns application health status

### **Main Application**
```
GET /
```
Main application interface

## 🎨 Color Science

### **Skin Tone Categories**
- **Very Light**: Delicate coloring, works with soft pastels
- **Light**: Luminous quality, versatile with many colors
- **Light-Medium**: Balanced tone, wide color range
- **Medium**: Natural warmth, complements earth tones
- **Medium-Dark**: Rich depth, stunning with bold colors
- **Dark**: Beautiful richness, shines with vibrant colors
- **Very Dark**: Striking depth, magnificent with bright colors

### **Undertone Analysis**
- **Warm**: Golden, yellow, peachy hues
- **Cool**: Pink, red, blue hues  
- **Neutral**: Balanced undertones, flexible color choices

### **Color Harmony Principles**
- **Complementary Colors**: Opposite colors on the color wheel
- **Analogous Colors**: Adjacent colors that blend harmoniously
- **Triadic Colors**: Three evenly spaced colors
- **Seasonal Palettes**: Colors that complement natural coloring

## 🔒 Security Features

- **File Validation**: Strict file type and size checking
- **Input Sanitization**: All user inputs are validated
- **Secure Upload**: Safe file handling and storage
- **Error Handling**: Graceful degradation and user feedback
- **Non-Root Container**: Security-hardened Docker deployment

## 🚀 Performance Optimizations

- **Async Processing**: Non-blocking image operations
- **Memory Efficient**: Optimized image handling and cleanup
- **Fast Algorithms**: Optimized computer vision algorithms
- **Lazy Loading**: Components load only when needed
- **Caching**: Efficient resource management

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- OpenCV community for computer vision tools
- NiceGUI team for the excellent Python web framework
- Color theory research and professional styling principles
- Beauty and fashion industry color analysis standards

---

**Built with ❤️ using Python and modern web technologies**