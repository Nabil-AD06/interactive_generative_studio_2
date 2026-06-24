from flask import Flask, render_template, request, send_file, send_from_directory, session, redirect, url_for
from werkzeug.utils import secure_filename
import os
from datetime import datetime

from config import PROJECT_ROOT, MEDIA_FOLDER, UPLOAD_FOLDER, GENERATED_FOLDER, AUDIO_FOLDER, AUDIO_AVAILABLE
from generative import generate_geometric_art, generate_fractal_tree, generate_spiral_pattern
from image_processing import apply_image_filter
from audio_processing import change_speed, change_pitch, add_echo, add_reverb, apply_audio_filter, generate_ambient_soundscape, create_spectrogram
from style_transfer import apply_neural_style_transfer_real
import data

app = Flask(__name__,
    template_folder=os.path.join(PROJECT_ROOT, 'frontend', 'templates'),
    static_folder=os.path.join(PROJECT_ROOT, 'frontend', 'static'),
    static_url_path='/static')
app.secret_key = 'your-secret-key-change-this'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['GENERATED_FOLDER'] = GENERATED_FOLDER
app.config['AUDIO_FOLDER'] = AUDIO_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(GENERATED_FOLDER, exist_ok=True)
os.makedirs(AUDIO_FOLDER, exist_ok=True)

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
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'art_{timestamp}.png'
        folder = os.path.abspath(GENERATED_FOLDER)
        os.makedirs(folder, exist_ok=True)
        filepath = os.path.join(folder, filename)
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
                original_path = os.path.join(UPLOAD_FOLDER, original_filename)
                file.save(original_path)
                session['original_image'] = original_filename
                session['processed_image'] = None
                return redirect(url_for('image_processor'))
        elif 'filter' in request.form:
            filter_type = request.form.get('filter')
            original = session.get('original_image')
            if original:
                original_path = os.path.join(UPLOAD_FOLDER, original)
                processed_img = apply_image_filter(original_path, filter_type)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                processed_filename = f'processed_{timestamp}.png'
                processed_path = os.path.join(UPLOAD_FOLDER, processed_filename)
                processed_img.save(processed_path)
                session['processed_image'] = processed_filename
                return redirect(url_for('image_processor'))
    original = session.get('original_image')
    processed = session.get('processed_image')
    return render_template('image_processor.html', original_image=original, processed_image=processed)

@app.route('/gallery')
def gallery():
    generated_images = []
    if os.path.exists(GENERATED_FOLDER):
        for filename in os.listdir(GENERATED_FOLDER):
            if filename.endswith(('.png', '.jpg', '.jpeg')):
                generated_images.append({'filename': filename, 'path': f"generated/{filename}", 'type': 'generated'})
    processed_images = []
    if os.path.exists(UPLOAD_FOLDER):
        for filename in os.listdir(UPLOAD_FOLDER):
            if filename.startswith('processed_') and filename.endswith(('.png', '.jpg', '.jpeg')):
                processed_images.append({'filename': filename, 'path': f"uploads/{filename}", 'type': 'processed'})
    styled_images = []
    if os.path.exists(UPLOAD_FOLDER):
        for filename in os.listdir(UPLOAD_FOLDER):
            if filename.startswith('styled_') and filename.endswith(('.png', '.jpg', '.jpeg')):
                styled_images.append({'filename': filename, 'path': f"uploads/{filename}", 'type': 'styled'})
    all_images = generated_images + processed_images + styled_images
    return render_template('gallery.html', generated_images=generated_images, processed_images=processed_images, styled_images=styled_images, all_images=all_images)

@app.route('/audio-processor', methods=['GET', 'POST'])
def audio_processor():
    if not AUDIO_AVAILABLE:
        return render_template('audio_unavailable.html')
    if request.method == 'POST':
        if 'audio' in request.files:
            file = request.files['audio']
            if file.filename != '':
                filename = secure_filename(file.filename)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                original_filename = f'original_{timestamp}_{filename}'
                original_path = os.path.join(AUDIO_FOLDER, original_filename)
                file.save(original_path)
                session['original_audio'] = original_filename
                session['processed_audio'] = None
                session['spectrogram'] = None
                return redirect(url_for('audio_processor'))
        elif 'effect' in request.form:
            effect = request.form.get('effect')
            original = session.get('original_audio')
            if original:
                original_path = os.path.join(AUDIO_FOLDER, original)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                processed_filename = f'processed_{timestamp}.mp3'
                processed_path = os.path.join(AUDIO_FOLDER, processed_filename)
                try:
                    if effect == 'speed_up':
                        processed = change_speed(original_path, 1.5)
                    elif effect == 'slow_down':
                        processed = change_speed(original_path, 0.75)
                    elif effect == 'pitch_up':
                        processed = change_pitch(original_path, 4, AUDIO_FOLDER)
                    elif effect == 'pitch_down':
                        processed = change_pitch(original_path, -4, AUDIO_FOLDER)
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
                    processed.export(processed_path, format='mp3')
                    session['processed_audio'] = processed_filename
                    spectrogram_file = create_spectrogram(processed_path, GENERATED_FOLDER)
                    session['spectrogram'] = spectrogram_file
                except Exception as e:
                    print(f"Error processing audio: {e}")
                    session['audio_error'] = "Erreur lors du traitement audio. Assurez-vous que FFmpeg est installé (lancez install_ffmpeg.bat)."
                return redirect(url_for('audio_processor'))
        elif 'generate_ambient' in request.form:
            duration = int(request.form.get('duration', 10)) * 1000
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            ambient_filename = f'ambient_{timestamp}.mp3'
            ambient_path = os.path.join(AUDIO_FOLDER, ambient_filename)
            try:
                ambient = generate_ambient_soundscape(duration, AUDIO_FOLDER)
                ambient.export(ambient_path, format='mp3')
                session['processed_audio'] = ambient_filename
                spectrogram_file = create_spectrogram(ambient_path, GENERATED_FOLDER)
                session['spectrogram'] = spectrogram_file
            except Exception as e:
                print(f"Error generating ambient: {e}")
                session['audio_error'] = "Erreur lors de la génération. FFmpeg est peut-être manquant (lancez install_ffmpeg.bat)."
            return redirect(url_for('audio_processor'))
    original = session.get('original_audio')
    processed = session.get('processed_audio')
    spectrogram = session.get('spectrogram')
    error = session.pop('audio_error', None)
    return render_template('audio_processor.html', original_audio=original, processed_audio=processed, spectrogram=spectrogram, audio_error=error)

@app.route('/style-transfer', methods=['GET', 'POST'])
def style_transfer():
    if request.method == 'POST':
        if 'image' in request.files:
            file = request.files['image']
            if file.filename != '':
                filename = secure_filename(file.filename)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                original_filename = f'original_{timestamp}_{filename}'
                original_path = os.path.join(UPLOAD_FOLDER, original_filename)
                file.save(original_path)
                session['style_original'] = original_filename
                session['style_processed'] = None
                return redirect(url_for('style_transfer'))
        elif 'style' in request.form:
            style = request.form.get('style')
            original = session.get('style_original')
            if original:
                original_path = os.path.join(UPLOAD_FOLDER, original)
                try:
                    styled_image = apply_neural_style_transfer_real(original_path, style)
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    styled_filename = f'styled_{timestamp}.png'
                    styled_path = os.path.join(UPLOAD_FOLDER, styled_filename)
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
    return render_template('style_transfer.html', original_image=original, styled_image=processed, style_error=error)

@app.route('/download/<path:filename>')
def download(filename):
    if filename.startswith('art_') or filename.endswith('_viz.png') or filename == 'spectrogram.png':
        filepath = os.path.join(GENERATED_FOLDER, filename)
    elif filename.startswith(('original_', 'processed_', 'ambient_', 'styled_')):
        if filename.endswith(('.mp3', '.wav', '.ogg')):
            filepath = os.path.join(AUDIO_FOLDER, filename)
        else:
            filepath = os.path.join(UPLOAD_FOLDER, filename)
    else:
        filepath = os.path.join(UPLOAD_FOLDER, filename)
    return send_file(filepath, as_attachment=True)

@app.route('/media/<path:filename>')
def media_file(filename):
    return send_from_directory(MEDIA_FOLDER, filename)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.static_folder), 'favicon.svg')

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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
