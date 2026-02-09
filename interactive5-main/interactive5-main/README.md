# 🎨 Interactive Generative Studio

A comprehensive web-based creative platform built with Python and Flask that combines generative art, data visualization, image processing, audio manipulation, and machine learning-powered style transfer.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📋 Table of Contents

- [Features](#-features)
- [Technologies](#-technologies)
- [Installation](#-installation)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [Module Details](#-module-details)
- [Troubleshooting](#-troubleshooting)

## ✨ Features

### 🌀 Generative Art Studio
- **Geometric Compositions**: Object-oriented design with Shape, Circle, Square, and Triangle classes
- **Fractal Trees**: Recursive tree generation with adjustable depth (1-10 levels)
- **Spiral Patterns**: Mathematical spiral designs with density control
- **Interactive Controls**: Real-time parameter adjustment with 6 color palettes
- **Export**: Download creations as high-quality PNG files

### 📊 Data Visualization
- **Wave Landscapes**: Transform temperature data into flowing compositions
- **Abstract Heatmaps**: 20x20 matrix visualizations with plasma colormap
- **Bar Compositions**: Artistic bar charts with viridis gradients
- **Technologies**: Pandas for data processing, Matplotlib for rendering

### 🖼️ Image Processing (25+ Effects)
- **Color Filters**: Grayscale, Sepia, Neon, Vintage, Warm/Cool temperature
- **Artistic Effects**: Watercolor, Oil Painting, Cartoon, Pencil Sketch
- **Distortions**: Glitch effects, Pixelation
- **Transformations**: Rotation, Mirroring, Flip
- **Advanced**: Edge detection, Emboss, Sharpen, Contour

### 🎵 Audio Processing
- **Speed Control**: Speed up (1.5x) or slow down (0.75x)
- **Pitch Shifting**: ±4 semitones using Librosa
- **Spatial Effects**: Echo (300ms delay) and Reverb simulation
- **Filters**: Low-pass, High-pass, Bass boost
- **Generation**: Ambient soundscape synthesizer
- **Visualization**: Real-time spectrogram analysis

### 🤖 Neural Style Transfer (ML Bonus)
- **Artist Styles**: Van Gogh, Monet, Picasso, Munch, Kandinsky
- **Technology**: TensorFlow Hub with arbitrary style transfer model
- **Fallback**: OpenCV artistic filters when TensorFlow unavailable
- **Resolution**: 800x600 optimized output

### 🎭 Gallery System
- Browse all generated artworks, processed images, and styled creations
- Organized by type with thumbnail previews
- Direct download functionality

## 🛠️ Technologies

### Core Technologies
- **Python 3.8+**: Main programming language
- **Flask 2.0+**: Web framework
- **Jinja2**: Template engine

### Image Processing
- **PIL/Pillow**: Basic image manipulation
- **OpenCV (cv2)**: Advanced image effects
- **NumPy**: Array operations

### Data & Visualization
- **Pandas**: Data processing
- **Matplotlib**: Chart generation
- **NumPy**: Numerical computations

### Audio Processing
- **PyDub**: Audio manipulation
- **Librosa**: Pitch shifting and analysis
- **SoundFile**: Audio I/O operations
- **FFmpeg**: Codec support

### Machine Learning (Optional)
- **TensorFlow 2.x**: Neural style transfer
- **TensorFlow Hub**: Pre-trained models

## 📦 Installation

### Step 1: Clone the Repository
```bash
git clone <your-repository-url>
cd interactive-generative-studio
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Python Dependencies
```bash
# Install core dependencies
pip install -r requirements.txt
```

### Step 4: Install FFmpeg (Required for Audio)

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
1. Download from [ffmpeg.org](https://ffmpeg.org/download.html)
2. Extract and add to PATH
3. Verify: `ffmpeg -version`

### Step 5: Install TensorFlow (Optional - For Neural Style Transfer)
```bash
# For CPU-only (lighter)
pip install tensorflow

# For GPU support
pip install tensorflow-gpu
```

## 🚀 Usage

### Starting the Application
```bash
python app.py
```

The application will start on `http://localhost:5000`

### Quick Start Guide

1. **Home Page** (`/`)
   - Overview of all available modules
   - Navigation to each feature

2. **Generative Art** (`/generative`)
   - Select art type (Geometric, Fractal, Spiral)
   - Adjust parameters (shapes, depth, density)
   - Choose color palette
   - Click "Generate Art"
   - Download or view in gallery

3. **Data Visualization** (`/data-viz`)
   - Select visualization type
   - Generate artistic data representation
   - Export as PNG

4. **Image Processing** (`/image-processor`)
   - Upload image (JPG, PNG, max 50MB)
   - Select from 25+ effects
   - Apply and download result

5. **Audio Processing** (`/audio-processor`)
   - Upload audio file (MP3, WAV, OGG)
   - Apply effects (speed, pitch, echo, etc.)
   - View spectrogram
   - Download processed audio

6. **Style Transfer** (`/style-transfer`)
   - Upload image
   - Choose artist style
   - Apply neural style transfer
   - Download stylized result

7. **Gallery** (`/gallery`)
   - Browse all your creations
   - Organized by type
   - Direct download access

## 📁 Project Structure

```
interactive-generative-studio/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── templates/                  # HTML templates
│   ├── base.html              # Base template
│   ├── home.html              # Homepage
│   ├── generative.html        # Generative art interface
│   ├── data_viz.html          # Data visualization
│   ├── image_processor.html   # Image processing
│   ├── audio_processor.html   # Audio processing
│   ├── audio_unavailable.html # Audio error page
│   ├── style_transfer.html    # Style transfer
│   └── gallery.html           # Gallery view
└── static/                     # Generated files (auto-created)
    ├── uploads/               # Uploaded images/audio
    ├── generated/             # Generated artworks
    └── audio/                 # Processed audio files
```

## 🔧 Module Details

### Generative Art (OOP Implementation)

**Classes:**
```python
class Shape:           # Base class
class Circle(Shape):   # Circular shapes
class Square(Shape):   # Square shapes
class Triangle(Shape): # Triangular shapes
```

**Algorithms:**
- Random positioning with loops and conditionals
- Recursive fractal generation
- Mathematical spiral patterns
- Color palette management

### Image Processing Pipeline

**Workflow:**
1. Upload → Secure filename → Resize (800x600)
2. Apply filter/effect
3. Save processed image
4. Display side-by-side comparison

**Key Functions:**
- `apply_image_filter()`: Master filter application
- `apply_glitch_effect()`: RGB channel shifting
- `apply_watercolor_effect()`: Bilateral + median filtering
- `apply_cartoon_effect()`: Edge detection + color quantization

### Audio Processing Pipeline

**Workflow:**
1. Upload → Validate format → Load with PyDub
2. Apply effect (speed/pitch/spatial/filter)
3. Generate spectrogram visualization
4. Export as MP3 (320kbps)

**Key Functions:**
- `change_speed()`: Frame rate manipulation
- `change_pitch()`: Librosa pitch shifting
- `add_echo()`: Delayed overlays
- `generate_ambient_soundscape()`: Sine wave synthesis

### Neural Style Transfer

**Implementation:**
- Primary: TensorFlow Hub arbitrary style transfer model
- Fallback: OpenCV artistic filters
- Input: Content image + Style selection
- Output: Stylized 800x600 image

## 🐛 Troubleshooting

### Audio Features Unavailable
**Error:** "Audio modules not available"
**Solution:**
```bash
pip install pydub librosa soundfile ffmpeg-python
# Then install FFmpeg for your OS
```

### TensorFlow Not Loading
**Error:** "TensorFlow not available"
**Solution:**
```bash
pip install tensorflow
# Or for GPU: pip install tensorflow-gpu
```

### Port Already in Use
**Error:** "Address already in use"
**Solution:**
```bash
# Change port in app.py:
app.run(debug=True, host='0.0.0.0', port=5001)
```

### File Upload Errors
**Error:** "File too large"
**Solution:** Check `MAX_CONTENT_LENGTH` in `app.py` (default: 50MB)

### Missing Dependencies
**Error:** "ModuleNotFoundError"
**Solution:**
```bash
pip install -r requirements.txt
```

## 📊 Performance Notes

- **Image Processing**: ~1-3 seconds per effect
- **Audio Processing**: ~2-5 seconds per effect
- **Style Transfer**: ~10-30 seconds (varies by hardware)
- **Generative Art**: Instant generation
- **Data Viz**: ~0.5-1 second

## 🔒 Security Features

- Secure filename handling with `werkzeug.utils.secure_filename`
- File size limits (50MB max)
- File type validation
- Session-based state management
- No database (stateless design)

## 🎓 Educational Value

This project demonstrates:
- **Object-Oriented Programming**: Shape classes hierarchy
- **Functional Programming**: Pure functions for effects
- **Data Processing**: Pandas/NumPy operations
- **Web Development**: Flask routing and templates
- **Signal Processing**: Audio manipulation
- **Computer Vision**: Image transformations
- **Machine Learning**: Neural style transfer
- **Software Engineering**: Modular architecture

## 📝 Requirements.txt

See `requirements.txt` for complete dependency list.

Core dependencies:
- flask>=2.0.0
- pillow>=9.0.0
- opencv-python>=4.5.0
- numpy>=1.21.0
- matplotlib>=3.5.0
- pandas>=1.3.0
- pydub>=0.25.0
- librosa>=0.9.0
- soundfile>=0.11.0
- tensorflow>=2.8.0 (optional)
- tensorflow-hub>=0.12.0 (optional)

## 👥 Credits

**Project:** Interactive Generative Studio  
**Course:** Digital Creativity using Python  
**Institution:** National School of Applied Sciences - Tangier  
**Year:** 2025

## 📄 License

This project is created for educational purposes as part of the Digital Creativity course.

## 🤝 Contributing

This is an academic project. For suggestions or improvements, please contact the project author.

---

**Built with ❤️ using Python, Flask, and Creative Coding Principles**