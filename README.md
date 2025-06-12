# 🎨 Color Harmony - AI Skin Tone & Color Analysis

A sophisticated web application that uses computer vision and color science to analyze skin tones from photos and provide personalized color recommendations. Built with NiceGUI, OpenCV, and advanced machine learning techniques.

## ✨ Features

- **📸 Smart Image Upload**: Drag-and-drop interface with support for JPG, PNG, and WebP formats
- **🔍 AI Skin Tone Analysis**: Advanced computer vision algorithms to detect and classify skin tones
- **🎨 Personalized Color Recommendations**: Curated color palettes based on your unique skin tone and undertones
- **🎛️ Real-time Skin Tone Adjustment**: Interactive controls to fine-tune brightness, warmth, saturation, and hue
- **🌈 Color Harmony Science**: Professional color theory applied to fashion and styling recommendations
- **📱 Responsive Design**: Beautiful, modern interface that works on desktop and mobile devices
- **⚡ Fast Processing**: Optimized algorithms for quick analysis and real-time adjustments

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- pip package manager

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd color-harmony
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python main.py
   ```

4. **Open your browser** and navigate to `http://localhost:8000`

## 🐳 Docker Deployment

### Build and run with Docker:

```bash
# Build the image
docker build -t color-harmony .

# Run the container
docker run -p 8000:8000 color-harmony
```

## ☁️ Deploy to Fly.io

1. **Install Fly CLI** and authenticate:
   ```bash
   curl -L https://fly.io/install.sh | sh
   flyctl auth login
   ```

2. **Deploy the application**:
   ```bash
   flyctl deploy
   ```

3. **Open your deployed app**:
   ```bash
   flyctl open
   ```

## 🎯 How It Works

### 1. Image Analysis
- Upload a clear photo of yourself or someone else
- The AI detects skin pixels using advanced color space analysis
- Face detection algorithms focus on the most relevant areas

### 2. Skin Tone Classification
- Analyzes dominant colors using K-means clustering
- Classifies skin tone into categories (Very Light to Very Dark)
- Determines undertones (Warm, Cool, or Neutral)

### 3. Color Recommendations
- Applies professional color theory principles
- Generates personalized color palettes
- Provides seasonal color analysis
- Suggests outfit combinations

### 4. Real-time Adjustments
- Interactive sliders for fine-tuning
- Preset adjustments for common preferences
- Live preview of changes

## 🎨 Color Science

The application uses advanced color science principles:

- **YCrCb Color Space**: For accurate skin detection
- **HSV Transformations**: For hue and saturation adjustments
- **Color Temperature**: For warm/cool tone modifications
- **K-means Clustering**: For dominant color extraction
- **Euclidean Distance**: For color matching and classification

## 🛠️ Technical Architecture

### Backend Components

- **NiceGUI**: Modern Python web framework for reactive UIs
- **OpenCV**: Computer vision and image processing
- **scikit-learn**: Machine learning for color clustering
- **PIL/Pillow**: Image manipulation and enhancement
- **NumPy/SciPy**: Numerical computations and color space transformations

### Project Structure

```
color-harmony/
├── main.py                 # Application entry point
├── app/
│   ├── main.py            # Main UI and page definitions
│   ├── config.py          # Application configuration
│   ├── components/        # Reusable UI components
│   └── services/          # Business logic services
├── core/                  # Core utilities and helpers
├── static/               # Static assets (CSS, images)
├── requirements.txt      # Python dependencies
├── dockerfile           # Container configuration
└── fly.toml            # Deployment configuration
```

## 🎛️ Configuration

### Environment Variables

Create a `.env` file to customize settings:

```env
PORT=8000
HOST=0.0.0.0
DEBUG=False
UPLOAD_DIR=static/uploads
MAX_FILE_SIZE=10485760
ALLOWED_EXTENSIONS=jpg,jpeg,png,webp
```

### Image Processing Settings

- **Max Image Size**: 1024x1024 pixels (configurable)
- **Supported Formats**: JPG, JPEG, PNG, WebP
- **Max File Size**: 10MB (configurable)
- **Processing Timeout**: 30 seconds

## 🔒 Security Features

- **File Validation**: Strict image format checking
- **Size Limits**: Prevents oversized uploads
- **Input Sanitization**: Safe filename handling
- **Error Handling**: Graceful failure management
- **CORS Protection**: Secure cross-origin requests

## 🚀 Performance Optimizations

- **Async Processing**: Non-blocking image operations
- **Image Resizing**: Automatic optimization for large images
- **Efficient Algorithms**: Optimized color analysis pipelines
- **Memory Management**: Proper cleanup of image resources
- **Caching**: Smart caching of processed results

## 🎨 UI/UX Features

- **Modern Design**: Clean, professional interface
- **Responsive Layout**: Mobile-first design approach
- **Interactive Elements**: Smooth animations and transitions
- **Accessibility**: WCAG compliance and keyboard navigation
- **Dark Mode Support**: Automatic theme detection
- **Loading States**: Clear feedback during processing

## 🧪 Testing

Run the test suite:

```bash
python -m pytest tests/
```

## 📊 API Endpoints

- `GET /` - Main application interface
- `GET /health` - Health check endpoint
- `POST /upload` - Image upload handling (internal)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Color theory research from fashion and beauty industry experts
- Computer vision techniques from academic research
- UI/UX inspiration from leading beauty and fashion applications

## 📞 Support

For support, feature requests, or bug reports, please open an issue on GitHub.

---

**Color Harmony** - Discover your perfect colors with AI-powered analysis! 🎨✨