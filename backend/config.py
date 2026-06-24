import os
import subprocess

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

backend_bin = os.path.join(PROJECT_ROOT, 'backend')
if os.path.isdir(backend_bin):
    os.environ['PATH'] = backend_bin + os.pathsep + os.environ.get('PATH', '')

try:
    from pydub import AudioSegment
    AUDIO_AVAILABLE = True
    for exe in ('ffmpeg', 'ffprobe'):
        fp = subprocess.run(['where', exe], capture_output=True, text=True, shell=True)
        print(f"[AUDIO] {exe} : {fp.stdout.strip() if fp.returncode == 0 else 'introuvable'}")
except ImportError:
    AUDIO_AVAILABLE = False
    print("[AUDIO] pydub non installe")

try:
    import tensorflow as tf
    import tensorflow_hub as hub
    TF_AVAILABLE = True
    print("[TF] TensorFlow loaded - Real Neural Style Transfer enabled")
    hub_model = hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2')
except Exception:
    TF_AVAILABLE = False
    hub_model = None
    print("[TF] TensorFlow not available - Using OpenCV artistic filters as fallback")

MEDIA_FOLDER = os.path.join(PROJECT_ROOT, 'media')
UPLOAD_FOLDER = os.path.join(MEDIA_FOLDER, 'uploads')
GENERATED_FOLDER = os.path.join(MEDIA_FOLDER, 'generated')
AUDIO_FOLDER = os.path.join(MEDIA_FOLDER, 'audio')
