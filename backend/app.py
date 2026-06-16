from flask import Flask, render_template, request, send_file, send_from_directory, session, redirect, url_for
from werkzeug.utils import secure_filename
import os
import sys
import io
import base64
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance, ImageOps
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import random
import math
from datetime import datetime

# Ajouter backend/ au PATH avant d'importer pydub pour que ffmpeg/ffprobe soient trouvés
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
backend_bin = os.path.join(PROJECT_ROOT, 'backend')
if os.path.isdir(backend_bin):
    os.environ['PATH'] = backend_bin + os.pathsep + os.environ.get('PATH', '')

try:
    from pydub import AudioSegment
    from pydub.effects import speedup, low_pass_filter, high_pass_filter
    import librosa
    import soundfile as sf
    AUDIO_AVAILABLE = True
except ImportError:
    AUDIO_AVAILABLE = False
    print("⚠️ Audio modules not available. Audio features will be disabled.")

import cv2

# TensorFlow for REAL Neural Style Transfer
try:
    import tensorflow as tf
    import tensorflow_hub as hub
    TF_AVAILABLE = True
    print("[TF] TensorFlow loaded - Real Neural Style Transfer enabled")
except ImportError:
    TF_AVAILABLE = False
    print("[TF] TensorFlow not available - Using OpenCV artistic filters as fallback")

# Verifier que ffmpeg/ffprobe sont trouvables via le PATH
if AUDIO_AVAILABLE:
    import subprocess
    for exe in ('ffmpeg', 'ffprobe'):
        fp = subprocess.run(['where', exe], capture_output=True, text=True, shell=True)
        print(f"[AUDIO] {exe} : {fp.stdout.strip() if fp.returncode == 0 else 'introuvable'}")

app = Flask(__name__,
    template_folder=os.path.join(PROJECT_ROOT, 'frontend', 'templates'),
    static_folder=os.path.join(PROJECT_ROOT, 'frontend', 'static'),
    static_url_path='/static')
app.secret_key = 'your-secret-key-change-this'

MEDIA_FOLDER = os.path.join(PROJECT_ROOT, 'media')
app.config['UPLOAD_FOLDER'] = os.path.join(MEDIA_FOLDER, 'uploads')
app.config['GENERATED_FOLDER'] = os.path.join(MEDIA_FOLDER, 'generated')
app.config['AUDIO_FOLDER'] = os.path.join(MEDIA_FOLDER, 'audio')
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024

# Create directories
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['GENERATED_FOLDER'], exist_ok=True)
os.makedirs(app.config['AUDIO_FOLDER'], exist_ok=True)

# Load TensorFlow Hub model for REAL Neural Style Transfer
if TF_AVAILABLE:
    try:
        print("📥 Loading Neural Style Transfer model from TensorFlow Hub...")
        hub_model = hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2')
        print("✅ Neural Style Transfer model loaded successfully!")
    except Exception as e:
        print(f"⚠️ Could not load TF Hub model: {e}")
        hub_model = None
        TF_AVAILABLE = False
else:
    hub_model = None

# ==================== Shape Classes (OOP) ====================

class Shape:
    """Base class for all shapes"""
    def __init__(self, x, y, size, color):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
    
    def draw(self, draw_obj):
        raise NotImplementedError("Subclasses must implement draw()")

class Circle(Shape):
    """Circle shape"""
    def draw(self, draw_obj):
        draw_obj.ellipse([
            self.x - self.size, self.y - self.size,
            self.x + self.size, self.y + self.size
        ], fill=self.color)

class Square(Shape):
    """Square shape"""
    def draw(self, draw_obj):
        draw_obj.rectangle([
            self.x - self.size, self.y - self.size,
            self.x + self.size, self.y + self.size
        ], fill=self.color)

class Triangle(Shape):
    """Triangle shape"""
    def draw(self, draw_obj):
        points = [
            (self.x, self.y - self.size),
            (self.x - self.size, self.y + self.size),
            (self.x + self.size, self.y + self.size)
        ]
        draw_obj.polygon(points, fill=self.color)

# ==================== Generative Art Functions ====================

def get_color_palette(palette_name):
    """Return color palette"""
    palettes = {
        'vibrant': ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8'],
        'pastel': ['#FFB3BA', '#BAFFC9', '#BAE1FF', '#FFFFBA', '#FFD9BA'],
        'neon': ['#FF10F0', '#00F0FF', '#FFFF00', '#FF1010', '#10FF10'],
        'earth': ['#8B4513', '#228B22', '#DEB887', '#6B8E23', '#CD853F'],
        'ocean': ['#006994', '#1E88E5', '#42A5F5', '#64B5F6', '#90CAF9'],
        'sunset': ['#FF6B35', '#F7931E', '#FDC830', '#F37335', '#C73E1D']
    }
    return palettes.get(palette_name, palettes['vibrant'])

def generate_geometric_art(num_shapes, palette):
    """Generate geometric art using OOP"""
    width, height = 800, 600
    img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(img, 'RGBA')
    
    colors = get_color_palette(palette)
    shape_classes = [Circle, Square, Triangle]
    
    for _ in range(num_shapes):
        x = random.randint(50, width - 50)
        y = random.randint(50, height - 50)
        size = random.randint(15, 60)
        color = random.choice(colors)
        
        shape_class = random.choice(shape_classes)
        shape = shape_class(x, y, size, color)
        shape.draw(draw)
    
    return img

# ==================== Audio Processing Functions ====================

def change_speed(audio_path, speed_factor):
    """Change audio speed"""
    audio = AudioSegment.from_file(audio_path)
    
    if speed_factor > 1.0:
        # Speed up
        faster_audio = speedup(audio, playback_speed=speed_factor)
        return faster_audio
    else:
        # Slow down by changing frame rate
        slower_audio = audio._spawn(audio.raw_data, overrides={
            "frame_rate": int(audio.frame_rate * speed_factor)
        })
        return slower_audio.set_frame_rate(audio.frame_rate)

def change_pitch(audio_path, semitones):
    """Change audio pitch using librosa"""
    y, sr = librosa.load(audio_path, sr=None)
    
    # Pitch shift
    y_shifted = librosa.effects.pitch_shift(y, sr=sr, n_steps=semitones)
    
    # Save to temporary file
    temp_path = os.path.join(app.config['AUDIO_FOLDER'], 'temp_pitch.wav')
    sf.write(temp_path, y_shifted, sr)
    
    return AudioSegment.from_wav(temp_path)

def add_echo(audio_path, delay_ms=300, decay=0.5):
    """Add echo effect"""
    audio = AudioSegment.from_file(audio_path)
    
    # Create echo
    echo = audio - (decay * 10)  # Reduce volume for echo
    
    # Overlay echo with delay
    output = audio.overlay(echo, position=delay_ms)
    
    # Add multiple echoes
    for i in range(2, 4):
        echo = echo - (decay * 5)
        output = output.overlay(echo, position=delay_ms * i)
    
    return output

def add_reverb(audio_path):
    """Simulate reverb effect"""
    audio = AudioSegment.from_file(audio_path)
    
    # Create multiple delayed copies with decreasing volume
    reverb = audio
    delays = [50, 100, 150, 200, 250, 300]
    
    for i, delay in enumerate(delays):
        decay = 0.6 ** (i + 1)
        echo = audio - (decay * 15)
        reverb = reverb.overlay(echo, position=delay)
    
    return reverb

def layer_audio(audio_paths):
    """Layer multiple audio clips"""
    if not audio_paths or len(audio_paths) == 0:
        return None
    
    # Load first audio
    layered = AudioSegment.from_file(audio_paths[0])
    
    # Overlay other audios
    for audio_path in audio_paths[1:]:
        audio = AudioSegment.from_file(audio_path)
        # Match length to longest
        if len(audio) < len(layered):
            audio = audio + AudioSegment.silent(duration=len(layered) - len(audio))
        elif len(audio) > len(layered):
            layered = layered + AudioSegment.silent(duration=len(audio) - len(layered))
        
        layered = layered.overlay(audio)
    
    return layered

def generate_ambient_soundscape(duration_ms=10000):
    """Generate ambient soundscape"""
    # Generate multiple sine waves at different frequencies
    sample_rate = 44100
    duration_s = duration_ms / 1000
    
    # Create base drone
    t = np.linspace(0, duration_s, int(sample_rate * duration_s))
    
    # Multiple harmonic layers
    frequencies = [110, 165, 220, 330, 440]  # A2, E3, A3, E4, A4
    audio_data = np.zeros_like(t)
    
    for i, freq in enumerate(frequencies):
        # Add some variation
        amplitude = 0.3 / (i + 1)
        wave = amplitude * np.sin(2 * np.pi * freq * t)
        
        # Add slow modulation
        modulation = 0.3 + 0.2 * np.sin(2 * np.pi * 0.1 * t)
        wave = wave * modulation
        
        audio_data += wave
    
    # Add some noise for texture
    noise = np.random.normal(0, 0.02, len(audio_data))
    audio_data += noise
    
    # Normalize
    audio_data = audio_data / np.max(np.abs(audio_data)) * 0.8
    
    # Convert to 16-bit PCM
    audio_data = (audio_data * 32767).astype(np.int16)
    
    # Save to temporary file
    temp_path = os.path.join(app.config['AUDIO_FOLDER'], 'temp_ambient.wav')
    sf.write(temp_path, audio_data, sample_rate)
    
    return AudioSegment.from_wav(temp_path)

def apply_audio_filter(audio_path, filter_type):
    """Apply audio filters"""
    audio = AudioSegment.from_file(audio_path)
    
    if filter_type == 'lowpass':
        return low_pass_filter(audio, 1000)
    elif filter_type == 'highpass':
        return high_pass_filter(audio, 1000)
    elif filter_type == 'bass_boost':
        # Boost low frequencies
        return audio.low_pass_filter(300).apply_gain(5) + audio.high_pass_filter(300)
    else:
        return audio

def create_spectrogram(audio_path):
    """Create spectrogram visualization"""
    y, sr = librosa.load(audio_path, sr=None, duration=30)
    
    # Create spectrogram
    D = librosa.stft(y)
    S_db = librosa.amplitude_to_db(np.abs(D), ref=np.max)
    
    fig, ax = plt.subplots(figsize=(12, 6), facecolor='#1a1a2e')
    ax.set_facecolor('#1a1a2e')
    
    img = librosa.display.specshow(S_db, sr=sr, x_axis='time', y_axis='hz', 
                                    ax=ax, cmap='plasma')
    
    ax.set_title('Audio Spectrogram', fontsize=18, color='white', pad=20)
    ax.set_xlabel('Time (s)', color='white', fontsize=12)
    ax.set_ylabel('Frequency (Hz)', color='white', fontsize=12)
    ax.tick_params(colors='white')
    
    cbar = plt.colorbar(img, ax=ax, format='%+2.0f dB')
    cbar.ax.tick_params(colors='white')
    cbar.set_label('Amplitude (dB)', color='white', fontsize=12)
    
    plt.tight_layout()
    
    filepath = os.path.join(app.config['GENERATED_FOLDER'], 'spectrogram.png')
    plt.savefig(filepath, facecolor='#1a1a2e', dpi=100)
    plt.close()
    
    return 'spectrogram.png'

# ==================== Style Transfer (REAL NEURAL NETWORK - ML BONUS) ====================

# Predefined style images (embedded in code as base64 or URLs)
STYLE_PRESETS = {
    'van_gogh': 'starry_night',  # Will use stylization
    'monet': 'impression_sunrise',
    'picasso': 'abstract_cubist',
    'munch': 'the_scream',
    'kandinsky': 'composition_vii'
}

def load_img(path_to_img, max_dim=512):
    """Load and preprocess image for neural network"""
    img = Image.open(path_to_img)
    img = img.convert('RGB')
    
    # Resize maintaining aspect ratio
    long_dim = max(img.size)
    scale = max_dim / long_dim
    new_size = tuple([int(dim * scale) for dim in img.size])
    img = img.resize(new_size, Image.Resampling.LANCZOS)
    
    # Convert to tensor
    img_array = np.array(img)
    img_array = img_array[np.newaxis, ...]
    
    if TF_AVAILABLE:
        img_array = img_array.astype(np.float32) / 255.0
    
    return img_array

def tensor_to_image(tensor):
    """Convert tensor to PIL Image"""
    if TF_AVAILABLE:
        tensor = tensor * 255
        tensor = np.array(tensor, dtype=np.uint8)
        if np.ndim(tensor) > 3:
            tensor = tensor[0]
    return Image.fromarray(tensor)

def apply_neural_style_transfer_real(content_path, style_type='van_gogh'):
    """
    REAL Neural Style Transfer using TensorFlow Hub
    Uses pre-trained arbitrary style transfer model
    """
    if not TF_AVAILABLE or hub_model is None:
        print("⚠️ TensorFlow not available, using fallback artistic filters")
        return apply_style_transfer_fallback(content_path, style_type)
    
    try:
        print(f"🎨 Applying REAL Neural Style Transfer with {style_type}...")
        
        # Load content image
        content_image = load_img(content_path)
        
        # Create style image (we'll use OpenCV filters to generate style patterns)
        # In production, you'd use actual paintings from Van Gogh, Monet, etc.
        style_image = create_style_pattern(style_type)
        
        # Apply neural style transfer using TensorFlow Hub model
        stylized_image = hub_model(tf.constant(content_image), tf.constant(style_image))[0]
        
        # Convert back to PIL Image
        result = tensor_to_image(stylized_image.numpy())
        
        print("✅ Neural Style Transfer completed successfully!")
        return result
        
    except Exception as e:
        print(f"❌ Error in neural style transfer: {e}")
        print("   Using fallback artistic filters...")
        return apply_style_transfer_fallback(content_path, style_type)

def create_style_pattern(style_type, size=512):
    """
    Create artistic style pattern for neural network
    In production, you would load actual paintings
    """
    # Create a synthetic artistic pattern
    img = np.zeros((size, size, 3), dtype=np.float32)
    
    if style_type == 'van_gogh':
        # Swirling patterns like Starry Night
        for i in range(size):
            for j in range(size):
                img[i, j] = [
                    0.2 + 0.3 * np.sin(i * 0.05 + j * 0.03),
                    0.3 + 0.4 * np.cos(i * 0.03 + j * 0.05),
                    0.5 + 0.5 * np.sin(i * 0.04 + j * 0.04)
                ]
    
    elif style_type == 'monet':
        # Soft impressionist colors
        for i in range(size):
            for j in range(size):
                img[i, j] = [
                    0.4 + 0.3 * np.random.random(),
                    0.5 + 0.2 * np.random.random(),
                    0.6 + 0.3 * np.random.random()
                ]
    
    elif style_type == 'picasso':
        # Geometric patterns
        for i in range(size):
            for j in range(size):
                img[i, j] = [
                    0.7 if (i + j) % 40 < 20 else 0.3,
                    0.5 if i % 30 < 15 else 0.2,
                    0.4 if j % 25 < 12 else 0.6
                ]
    
    else:
        # Default artistic pattern
        for i in range(size):
            for j in range(size):
                img[i, j] = [
                    0.5 + 0.5 * np.sin(i * 0.02),
                    0.5 + 0.5 * np.cos(j * 0.02),
                    0.5
                ]
    
    # Add to batch dimension
    return img[np.newaxis, ...]

def apply_style_transfer_fallback(content_image_path, style_type='van_gogh'):
    """
    Fallback using OpenCV artistic filters (when TensorFlow not available)
    """
    content_img = cv2.imread(content_image_path)
    if content_img is None:
        try:
            from PIL import Image as PILImage
            pil_img = PILImage.open(content_image_path).convert('RGB')
            pil_img = pil_img.resize((800, 600))
            content_img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
        except Exception as e:
            raise RuntimeError(f"Could not load image: {e}")
    else:
        content_img = cv2.resize(content_img, (800, 600))
    
    if style_type == 'van_gogh':
        styled = cv2.stylization(content_img, sigma_s=60, sigma_r=0.6)
        styled = cv2.detailEnhance(styled, sigma_s=10, sigma_r=0.15)
        
    elif style_type == 'monet':
        styled = cv2.edgePreservingFilter(content_img, flags=1, sigma_s=60, sigma_r=0.4)
        styled = cv2.detailEnhance(styled, sigma_s=10, sigma_r=0.15)
        
    elif style_type == 'picasso':
        gray = cv2.cvtColor(content_img, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        styled = cv2.addWeighted(content_img, 0.7, edges_colored, 0.3, 0)
        styled = cv2.bilateralFilter(styled, 9, 75, 75)
        
    elif style_type == 'munch':
        styled = cv2.stylization(content_img, sigma_s=150, sigma_r=0.25)
        lab = cv2.cvtColor(styled, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
        l = clahe.apply(l)
        styled = cv2.merge([l, a, b])
        styled = cv2.cvtColor(styled, cv2.COLOR_LAB2BGR)
        
    elif style_type == 'kandinsky':
        styled = cv2.pyrMeanShiftFiltering(content_img, 21, 51)
        styled = cv2.detailEnhance(styled, sigma_s=10, sigma_r=0.5)
    
    styled_rgb = cv2.cvtColor(styled, cv2.COLOR_BGR2RGB)
    return Image.fromarray(styled_rgb)

def generate_fractal_tree(depth):
    """Generate fractal tree"""
    width, height = 800, 600
    img = Image.new('RGB', (width, height), '#1a1a2e')
    draw = ImageDraw.Draw(img)
    
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8']
    
    def draw_branch(x, y, length, angle, level):
        if level == 0:
            return
        
        x2 = x + length * math.cos(angle)
        y2 = y + length * math.sin(angle)
        
        color = colors[level % len(colors)]
        draw.line([(x, y), (x2, y2)], fill=color, width=max(1, level))
        
        draw_branch(x2, y2, length * 0.7, angle - 0.5, level - 1)
        draw_branch(x2, y2, length * 0.7, angle + 0.5, level - 1)
    
    draw_branch(width // 2, height - 50, 100, -math.pi / 2, depth)
    return img

def generate_spiral_pattern(density):
    """Generate spiral pattern"""
    width, height = 800, 600
    img = Image.new('RGB', (width, height), '#0f0f23')
    draw = ImageDraw.Draw(img, 'RGBA')
    
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8']
    center_x, center_y = width // 2, height // 2
    
    for i in range(0, 360 * density, 2):
        angle = math.radians(i)
        radius = i * 0.3
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        
        color = colors[(i // 30) % len(colors)]
        size = 3 + (i % 50) // 10
        draw.ellipse([x-size, y-size, x+size, y+size], fill=color)
    
    return img

# ==================== Data Visualization Functions ====================

def create_wave_visualization():
    """Create artistic wave visualization"""
    dates = pd.date_range('2024-01-01', periods=60, freq='D')
    temps = 15 + 10 * np.sin(np.linspace(0, 4 * np.pi, 60)) + np.random.randn(60) * 2
    
    fig, ax = plt.subplots(figsize=(12, 6), facecolor='#1a1a2e')
    ax.set_facecolor('#1a1a2e')
    
    for i in range(len(temps) - 1):
        color = plt.cm.coolwarm((temps[i] - temps.min()) / (temps.max() - temps.min()))
        ax.fill_between([i, i + 1], [0, 0], [temps[i], temps[i + 1]], 
                        color=color, alpha=0.8)
    
    ax.plot(temps, color='white', linewidth=3, alpha=0.9)
    ax.set_ylim(0, max(temps) * 1.1)
    ax.set_title('Temperature Wave Landscape', fontsize=18, color='white', pad=20)
    ax.set_xlabel('Days', color='white', fontsize=12)
    ax.set_ylabel('Temperature (°C)', color='white', fontsize=12)
    ax.tick_params(colors='white')
    ax.spines['bottom'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(True, alpha=0.2, color='white')
    
    plt.tight_layout()
    
    filepath = os.path.join(app.config['GENERATED_FOLDER'], 'wave_viz.png')
    plt.savefig(filepath, facecolor='#1a1a2e', dpi=100)
    plt.close()
    
    return 'wave_viz.png'

def create_heatmap_visualization():
    """Create abstract heatmap"""
    data = np.random.rand(20, 20) * 100
    
    fig, ax = plt.subplots(figsize=(10, 8), facecolor='#1a1a2e')
    im = ax.imshow(data, cmap='plasma', aspect='auto', interpolation='bilinear')
    
    ax.set_title('Abstract Data Heatmap', fontsize=18, color='white', pad=20)
    ax.tick_params(colors='white')
    ax.spines['bottom'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    cbar = plt.colorbar(im, ax=ax)
    cbar.ax.tick_params(colors='white')
    cbar.set_label('Values', color='white', fontsize=12)
    
    plt.tight_layout()
    
    filepath = os.path.join(app.config['GENERATED_FOLDER'], 'heatmap_viz.png')
    plt.savefig(filepath, facecolor='#1a1a2e', dpi=100)
    plt.close()
    
    return 'heatmap_viz.png'

def create_bar_visualization():
    """Create abstract bar chart"""
    categories = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    values = np.random.randint(30, 100, size=len(categories))
    
    fig, ax = plt.subplots(figsize=(12, 6), facecolor='#1a1a2e')
    ax.set_facecolor('#1a1a2e')
    
    colors = plt.cm.viridis(np.linspace(0, 1, len(categories)))
    bars = ax.bar(categories, values, color=colors, edgecolor='white', linewidth=2)
    
    for bar, val in zip(bars, values):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2., height + 2,
                f'{val}', ha='center', va='bottom', fontweight='bold', 
                color='white', fontsize=12)
    
    ax.set_title('Abstract Data Composition', fontsize=18, color='white', pad=20)
    ax.set_ylabel('Values', color='white', fontsize=12)
    ax.tick_params(colors='white')
    ax.spines['bottom'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(True, alpha=0.2, axis='y', color='white')
    
    plt.tight_layout()
    
    filepath = os.path.join(app.config['GENERATED_FOLDER'], 'bar_viz.png')
    plt.savefig(filepath, facecolor='#1a1a2e', dpi=100)
    plt.close()
    
    return 'bar_viz.png'

# ==================== Image Processing Functions ====================

def apply_image_filter(image_path, filter_type):
    """Apply filter to image"""
    img = Image.open(image_path)
    img = img.resize((800, 600))
    
    # Color Filters
    if filter_type == 'grayscale':
        img = ImageOps.grayscale(img).convert('RGB')
    
    elif filter_type == 'sepia':
        grayscale = ImageOps.grayscale(img)
        sepia = Image.new('RGB', img.size)
        pixels = sepia.load()
        gray_pixels = grayscale.load()
        
        for i in range(img.size[0]):
            for j in range(img.size[1]):
                gray = gray_pixels[i, j]
                pixels[i, j] = (
                    min(255, int(gray * 1.0)),
                    min(255, int(gray * 0.95)),
                    min(255, int(gray * 0.82))
                )
        img = sepia
    
    elif filter_type == 'neon':
        enhancer = ImageEnhance.Color(img)
        img = enhancer.enhance(3.0)
        img = ImageEnhance.Brightness(img).enhance(1.2)
        img = ImageEnhance.Contrast(img).enhance(1.5)
    
    elif filter_type == 'invert':
        img = ImageOps.invert(img.convert('RGB'))
    
    # Artistic Distortions
    elif filter_type == 'glitch':
        img = apply_glitch_effect(img)
    
    elif filter_type == 'pixelate':
        small = img.resize((img.size[0] // 15, img.size[1] // 15), Image.NEAREST)
        img = small.resize((800, 600), Image.NEAREST)
    
    elif filter_type == 'watercolor':
        img = apply_watercolor_effect(img)
    
    elif filter_type == 'blur':
        img = img.filter(ImageFilter.GaussianBlur(radius=5))
    
    elif filter_type == 'oil_painting':
        img = apply_oil_painting_effect(img)
    
    # Advanced Effects with OpenCV
    elif filter_type == 'sharpen':
        img = img.filter(ImageFilter.SHARPEN)
    
    elif filter_type == 'edge':
        img = img.filter(ImageFilter.FIND_EDGES)
    
    elif filter_type == 'emboss':
        img = img.filter(ImageFilter.EMBOSS)
    
    elif filter_type == 'contour':
        img = img.filter(ImageFilter.CONTOUR)
    
    elif filter_type == 'cartoon':
        img = apply_cartoon_effect(img)
    
    elif filter_type == 'sketch':
        img = apply_sketch_effect(img)
    
    # Geometric Transformations
    elif filter_type == 'rotate_90':
        img = img.rotate(90, expand=True)
    
    elif filter_type == 'rotate_180':
        img = img.rotate(180)
    
    elif filter_type == 'flip_horizontal':
        img = ImageOps.mirror(img)
    
    elif filter_type == 'flip_vertical':
        img = ImageOps.flip(img)
    
    # Color Adjustments
    elif filter_type == 'vintage':
        img = apply_vintage_effect(img)
    
    elif filter_type == 'warm':
        img = apply_temperature_effect(img, warm=True)
    
    elif filter_type == 'cool':
        img = apply_temperature_effect(img, warm=False)
    
    elif filter_type == 'high_contrast':
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(2.0)
    
    return img

def apply_glitch_effect(img):
    """Apply glitch distortion effect"""
    img_array = np.array(img)
    height, width = img_array.shape[:2]
    
    # Random horizontal shifts
    for _ in range(10):
        y = random.randint(0, height - 20)
        shift = random.randint(-50, 50)
        if shift > 0:
            img_array[y:y+20, shift:] = img_array[y:y+20, :-shift]
        elif shift < 0:
            img_array[y:y+20, :shift] = img_array[y:y+20, -shift:]
    
    # Color channel shift
    if len(img_array.shape) == 3:
        shift_amount = random.randint(5, 15)
        img_array[:, shift_amount:, 0] = img_array[:, :-shift_amount, 0]  # Red channel
        img_array[:, :-shift_amount, 2] = img_array[:, shift_amount:, 2]  # Blue channel
    
    return Image.fromarray(img_array)

def apply_watercolor_effect(img):
    """Apply watercolor painting effect using OpenCV"""
    img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    
    # Apply bilateral filter for smoothing while preserving edges
    img_cv = cv2.bilateralFilter(img_cv, 9, 75, 75)
    
    # Apply median blur
    img_cv = cv2.medianBlur(img_cv, 5)
    
    # Reduce color palette
    img_cv = cv2.pyrMeanShiftFiltering(img_cv, 21, 51)
    
    img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
    return Image.fromarray(img_rgb)

def apply_oil_painting_effect(img):
    """Apply oil painting effect"""
    img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    
    # Apply bilateral filter multiple times
    for _ in range(3):
        img_cv = cv2.bilateralFilter(img_cv, 9, 100, 100)
    
    img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
    return Image.fromarray(img_rgb)

def apply_cartoon_effect(img):
    """Apply cartoon effect using OpenCV"""
    img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    
    # Edge detection
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)
    edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, 
                                   cv2.THRESH_BINARY, 9, 9)
    
    # Color quantization
    color = cv2.bilateralFilter(img_cv, 9, 250, 250)
    
    # Combine edges and color
    cartoon = cv2.bitwise_and(color, color, mask=edges)
    
    img_rgb = cv2.cvtColor(cartoon, cv2.COLOR_BGR2RGB)
    return Image.fromarray(img_rgb)

def apply_sketch_effect(img):
    """Apply pencil sketch effect"""
    img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    
    # Convert to grayscale
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    
    # Invert the grayscale image
    inverted = 255 - gray
    
    # Apply Gaussian blur
    blurred = cv2.GaussianBlur(inverted, (21, 21), 0)
    
    # Invert the blurred image
    inverted_blur = 255 - blurred
    
    # Create sketch by dividing gray by inverted blur
    sketch = cv2.divide(gray, inverted_blur, scale=256.0)
    
    # Convert to RGB
    sketch_rgb = cv2.cvtColor(sketch, cv2.COLOR_GRAY2RGB)
    return Image.fromarray(sketch_rgb)

def apply_vintage_effect(img):
    """Apply vintage photo effect"""
    # Apply sepia
    grayscale = ImageOps.grayscale(img)
    sepia = Image.new('RGB', img.size)
    pixels = sepia.load()
    gray_pixels = grayscale.load()
    
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            gray = gray_pixels[i, j]
            pixels[i, j] = (
                min(255, int(gray * 1.1)),
                min(255, int(gray * 0.9)),
                min(255, int(gray * 0.7))
            )
    
    # Reduce contrast and add slight blur
    enhancer = ImageEnhance.Contrast(sepia)
    sepia = enhancer.enhance(0.8)
    sepia = sepia.filter(ImageFilter.GaussianBlur(radius=1))
    
    return sepia

def apply_temperature_effect(img, warm=True):
    """Apply warm or cool temperature effect"""
    img_array = np.array(img, dtype=np.float32)
    
    if warm:
        # Increase red, decrease blue
        img_array[:, :, 0] = np.clip(img_array[:, :, 0] * 1.1, 0, 255)  # Red
        img_array[:, :, 2] = np.clip(img_array[:, :, 2] * 0.9, 0, 255)  # Blue
    else:
        # Decrease red, increase blue
        img_array[:, :, 0] = np.clip(img_array[:, :, 0] * 0.9, 0, 255)  # Red
        img_array[:, :, 2] = np.clip(img_array[:, :, 2] * 1.1, 0, 255)  # Blue
    
    return Image.fromarray(img_array.astype(np.uint8))

# ==================== Routes ====================

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/generative', methods=['GET', 'POST'])
def generative():
    if request.method == 'POST':
        art_type = request.form.get('art_type', 'geometric')
        
        if art_type == 'geometric':
            num_shapes = int(request.form.get('num_shapes', 50))
            palette = request.form.get('palette', 'vibrant')
            img = generate_geometric_art(num_shapes, palette)
        
        elif art_type == 'fractal':
            depth = int(request.form.get('depth', 8))
            img = generate_fractal_tree(depth)
        
        elif art_type == 'spiral':
            density = int(request.form.get('density', 3))
            img = generate_spiral_pattern(density)
        
        # Save image
        # Save image (FIX Windows path)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'art_{timestamp}.png'

        folder = os.path.abspath(app.config['GENERATED_FOLDER'])
        os.makedirs(folder, exist_ok=True)  # assure que le dossier existe

        filepath = os.path.join(folder, filename)
        print("Saving to:", filepath)  # debug

        img.save(filepath)
        
        session['last_generated'] = filename
        return redirect(url_for('generative'))
    
    last_image = session.get('last_generated')
    return render_template('generative.html', generated_image=last_image)

@app.route('/image-processor', methods=['GET', 'POST'])
def image_processor():
    if request.method == 'POST':
        if 'image' in request.files:
            file = request.files['image']
            if file.filename != '':
                filename = secure_filename(file.filename)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                original_filename = f'original_{timestamp}_{filename}'
                original_path = os.path.join(app.config['UPLOAD_FOLDER'], original_filename)
                file.save(original_path)
                
                session['original_image'] = original_filename
                session['processed_image'] = None
                return redirect(url_for('image_processor'))
        
        elif 'filter' in request.form:
            filter_type = request.form.get('filter')
            original = session.get('original_image')
            
            if original:
                original_path = os.path.join(app.config['UPLOAD_FOLDER'], original)
                processed_img = apply_image_filter(original_path, filter_type)
                
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                processed_filename = f'processed_{timestamp}.png'
                processed_path = os.path.join(app.config['UPLOAD_FOLDER'], processed_filename)
                processed_img.save(processed_path)
                
                session['processed_image'] = processed_filename
                return redirect(url_for('image_processor'))
    
    original = session.get('original_image')
    processed = session.get('processed_image')
    return render_template('image_processor.html', 
                          original_image=original, 
                          processed_image=processed)

@app.route('/gallery')
def gallery():
    # Get all generated images
    generated_images = []
    if os.path.exists(app.config['GENERATED_FOLDER']):
        for filename in os.listdir(app.config['GENERATED_FOLDER']):
            if filename.endswith(('.png', '.jpg', '.jpeg')):
                generated_images.append({
                    'filename': filename,
                    'path': f"generated/{filename}",
                    'type': 'generated'
                })
    
    # Get processed images
    processed_images = []
    if os.path.exists(app.config['UPLOAD_FOLDER']):
        for filename in os.listdir(app.config['UPLOAD_FOLDER']):
            if filename.startswith('processed_') and filename.endswith(('.png', '.jpg', '.jpeg')):
                processed_images.append({
                    'filename': filename,
                    'path': f"uploads/{filename}",
                    'type': 'processed'
                })
    
    # Get styled images
    styled_images = []
    if os.path.exists(app.config['UPLOAD_FOLDER']):
        for filename in os.listdir(app.config['UPLOAD_FOLDER']):
            if filename.startswith('styled_') and filename.endswith(('.png', '.jpg', '.jpeg')):
                styled_images.append({
                    'filename': filename,
                    'path': f"uploads/{filename}",
                    'type': 'styled'
                })
    
    all_images = generated_images + processed_images + styled_images
    
    return render_template('gallery.html', 
                          generated_images=generated_images,
                          processed_images=processed_images,
                          styled_images=styled_images,
                          all_images=all_images)

@app.route('/audio-processor', methods=['GET', 'POST'])
def audio_processor():
    if not AUDIO_AVAILABLE:
        return render_template('audio_unavailable.html')
    
    if request.method == 'POST':
        # Upload audio file
        if 'audio' in request.files:
            file = request.files['audio']
            if file.filename != '':
                filename = secure_filename(file.filename)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                original_filename = f'original_{timestamp}_{filename}'
                original_path = os.path.join(app.config['AUDIO_FOLDER'], original_filename)
                file.save(original_path)
                
                session['original_audio'] = original_filename
                session['processed_audio'] = None
                session['spectrogram'] = None
                return redirect(url_for('audio_processor'))
        
        # Process audio
        elif 'effect' in request.form:
            effect = request.form.get('effect')
            original = session.get('original_audio')
            
            if original:
                original_path = os.path.join(app.config['AUDIO_FOLDER'], original)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                processed_filename = f'processed_{timestamp}.mp3'
                processed_path = os.path.join(app.config['AUDIO_FOLDER'], processed_filename)
                
                try:
                    if effect == 'speed_up':
                        processed = change_speed(original_path, 1.5)
                    elif effect == 'slow_down':
                        processed = change_speed(original_path, 0.75)
                    elif effect == 'pitch_up':
                        processed = change_pitch(original_path, 4)
                    elif effect == 'pitch_down':
                        processed = change_pitch(original_path, -4)
                    elif effect == 'echo':
                        processed = add_echo(original_path)
                    elif effect == 'reverb':
                        processed = add_reverb(original_path)
                    elif effect == 'lowpass':
                        processed = apply_audio_filter(original_path, 'lowpass')
                    elif effect == 'highpass':
                        processed = apply_audio_filter(original_path, 'highpass')
                    elif effect == 'bass_boost':
                        processed = apply_audio_filter(original_path, 'bass_boost')
                    
                    # Export processed audio
                    processed.export(processed_path, format='mp3')
                    session['processed_audio'] = processed_filename
                    
                    # Generate spectrogram
                    spectrogram_file = create_spectrogram(processed_path)
                    session['spectrogram'] = spectrogram_file
                    
                except Exception as e:
                    print(f"Error processing audio: {e}")
                    session['audio_error'] = "Erreur lors du traitement audio. Assurez-vous que FFmpeg est installé (lancez install_ffmpeg.bat)."
                
                return redirect(url_for('audio_processor'))
        
        # Generate ambient soundscape
        elif 'generate_ambient' in request.form:
            duration = int(request.form.get('duration', 10)) * 1000
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            ambient_filename = f'ambient_{timestamp}.mp3'
            ambient_path = os.path.join(app.config['AUDIO_FOLDER'], ambient_filename)
            
            try:
                ambient = generate_ambient_soundscape(duration)
                ambient.export(ambient_path, format='mp3')
                
                session['processed_audio'] = ambient_filename
                
                # Generate spectrogram
                spectrogram_file = create_spectrogram(ambient_path)
                session['spectrogram'] = spectrogram_file
            except Exception as e:
                print(f"Error generating ambient: {e}")
                session['audio_error'] = "Erreur lors de la génération. FFmpeg est peut-être manquant (lancez install_ffmpeg.bat)."
            
            return redirect(url_for('audio_processor'))
    
    original = session.get('original_audio')
    processed = session.get('processed_audio')
    spectrogram = session.get('spectrogram')
    error = session.pop('audio_error', None)
    return render_template('audio_processor.html', 
                          original_audio=original, 
                          processed_audio=processed,
                          spectrogram=spectrogram,
                          audio_error=error)

@app.route('/style-transfer', methods=['GET', 'POST'])
def style_transfer():
    if request.method == 'POST':
        if 'image' in request.files:
            file = request.files['image']
            if file.filename != '':
                filename = secure_filename(file.filename)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                original_filename = f'original_{timestamp}_{filename}'
                original_path = os.path.join(app.config['UPLOAD_FOLDER'], original_filename)
                file.save(original_path)
                
                session['style_original'] = original_filename
                session['style_processed'] = None
                return redirect(url_for('style_transfer'))
        
        elif 'style' in request.form:
            style = request.form.get('style')
            original = session.get('style_original')
            
            if original:
                original_path = os.path.join(app.config['UPLOAD_FOLDER'], original)
                
                try:
                    styled_image = apply_neural_style_transfer_real(original_path, style)
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    styled_filename = f'styled_{timestamp}.png'
                    styled_path = os.path.join(app.config['UPLOAD_FOLDER'], styled_filename)
                    styled_image.save(styled_path)
                    
                    session['style_processed'] = styled_filename
                    session.pop('style_error', None)
                except Exception as e:
                    print(f"Error applying style: {e}")
                    session['style_error'] = f"Erreur lors de l'application du style : {str(e)}"
                
                return redirect(url_for('style_transfer'))
    
    original = session.get('style_original')
    processed = session.get('style_processed')
    error = session.pop('style_error', None)
    return render_template('style_transfer.html',
                          original_image=original,
                          styled_image=processed,
                          style_error=error)

@app.route('/download/<path:filename>')
def download(filename):
    """Download generated files"""
    if filename.startswith('art_') or filename.endswith('_viz.png') or filename == 'spectrogram.png':
        filepath = os.path.join(app.config['GENERATED_FOLDER'], filename)
    elif filename.startswith('original_') or filename.startswith('processed_') or filename.startswith('ambient_') or filename.startswith('styled_'):
        if filename.endswith(('.mp3', '.wav', '.ogg')):
            filepath = os.path.join(app.config['AUDIO_FOLDER'], filename)
        else:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    else:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    return send_file(filepath, as_attachment=True)

@app.route('/media/<path:filename>')
def media_file(filename):
    return send_from_directory(MEDIA_FOLDER, filename)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.static_folder), 'favicon.svg')
#==================================================
import data

@app.route("/data-viz")
def data_viz():
    model = request.args.get("model")
    img = None
    html_plot = None

    if model == "energy":
        img = data.energy_density_flow()
    elif model == "heatmap":
        img = data.weekly_heatmap()
    elif model == "mandala":
        img = data.seasonal_workout_mandala()
    elif model == "bubble":
        html_plot = data.interactive_bubble_chart()
    elif model == "sunburst":
        html_plot = data.interactive_sunburst()

    return render_template("data_viz.html", image=img, html_plot=html_plot)

#==================================================
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)