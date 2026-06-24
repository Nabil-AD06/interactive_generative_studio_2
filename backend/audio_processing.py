import os
import numpy as np
from pydub import AudioSegment
from pydub.effects import speedup, low_pass_filter, high_pass_filter
import librosa
import soundfile as sf
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def change_speed(audio_path, speed_factor):
    audio = AudioSegment.from_file(audio_path)
    if speed_factor > 1.0:
        return speedup(audio, playback_speed=speed_factor)
    else:
        slower = audio._spawn(audio.raw_data, overrides={"frame_rate": int(audio.frame_rate * speed_factor)})
        return slower.set_frame_rate(audio.frame_rate)

def change_pitch(audio_path, semitones, audio_folder):
    y, sr = librosa.load(audio_path, sr=None)
    y_shifted = librosa.effects.pitch_shift(y, sr=sr, n_steps=semitones)
    temp_path = os.path.join(audio_folder, 'temp_pitch.wav')
    sf.write(temp_path, y_shifted, sr)
    return AudioSegment.from_wav(temp_path)

def add_echo(audio_path, delay_ms=300, decay=0.5):
    audio = AudioSegment.from_file(audio_path)
    echo = audio - (decay * 10)
    output = audio.overlay(echo, position=delay_ms)
    for i in range(2, 4):
        echo = echo - (decay * 5)
        output = output.overlay(echo, position=delay_ms * i)
    return output

def add_reverb(audio_path):
    audio = AudioSegment.from_file(audio_path)
    reverb = audio
    delays = [50, 100, 150, 200, 250, 300]
    for i, delay in enumerate(delays):
        decay = 0.6 ** (i + 1)
        echo = audio - (decay * 15)
        reverb = reverb.overlay(echo, position=delay)
    return reverb

def apply_audio_filter(audio_path, filter_type):
    audio = AudioSegment.from_file(audio_path)
    if filter_type == 'lowpass':
        return low_pass_filter(audio, 1000)
    elif filter_type == 'highpass':
        return high_pass_filter(audio, 1000)
    elif filter_type == 'bass_boost':
        return audio.low_pass_filter(300).apply_gain(5) + audio.high_pass_filter(300)
    return audio

def generate_ambient_soundscape(duration_ms=10000, audio_folder=None):
    sample_rate = 44100
    duration_s = duration_ms / 1000
    t = np.linspace(0, duration_s, int(sample_rate * duration_s))
    frequencies = [110, 165, 220, 330, 440]
    audio_data = np.zeros_like(t)
    for i, freq in enumerate(frequencies):
        amplitude = 0.3 / (i + 1)
        wave = amplitude * np.sin(2 * np.pi * freq * t)
        modulation = 0.3 + 0.2 * np.sin(2 * np.pi * 0.1 * t)
        wave = wave * modulation
        audio_data += wave
    noise = np.random.normal(0, 0.02, len(audio_data))
    audio_data += noise
    audio_data = audio_data / np.max(np.abs(audio_data)) * 0.8
    audio_data = (audio_data * 32767).astype(np.int16)
    temp_path = os.path.join(audio_folder or os.getcwd(), 'temp_ambient.wav')
    sf.write(temp_path, audio_data, sample_rate)
    return AudioSegment.from_wav(temp_path)

def create_spectrogram(audio_path, output_dir):
    y, sr = librosa.load(audio_path, sr=None, duration=30)
    D = librosa.stft(y)
    S_db = librosa.amplitude_to_db(np.abs(D), ref=np.max)
    fig, ax = plt.subplots(figsize=(12, 6), facecolor='#1a1a2e')
    ax.set_facecolor('#1a1a2e')
    img = librosa.display.specshow(S_db, sr=sr, x_axis='time', y_axis='hz', ax=ax, cmap='plasma')
    ax.set_title('Audio Spectrogram', fontsize=18, color='white', pad=20)
    ax.set_xlabel('Time (s)', color='white', fontsize=12)
    ax.set_ylabel('Frequency (Hz)', color='white', fontsize=12)
    ax.tick_params(colors='white')
    cbar = plt.colorbar(img, ax=ax, format='%+2.0f dB')
    cbar.ax.tick_params(colors='white')
    cbar.set_label('Amplitude (dB)', color='white', fontsize=12)
    plt.tight_layout()
    filepath = os.path.join(output_dir, 'spectrogram.png')
    plt.savefig(filepath, facecolor='#1a1a2e', dpi=100)
    plt.close()
    return 'spectrogram.png'
