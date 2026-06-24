import numpy as np
import cv2
from PIL import Image
from config import TF_AVAILABLE, hub_model

STYLE_PRESETS = {
    'van_gogh': 'starry_night',
    'monet': 'impression_sunrise',
    'picasso': 'abstract_cubist',
    'munch': 'the_scream',
    'kandinsky': 'composition_vii'
}

def load_img(path_to_img, max_dim=512):
    img = Image.open(path_to_img)
    img = img.convert('RGB')
    long_dim = max(img.size)
    scale = max_dim / long_dim
    new_size = tuple([int(dim * scale) for dim in img.size])
    img = img.resize(new_size, Image.Resampling.LANCZOS)
    img_array = np.array(img)
    img_array = img_array[np.newaxis, ...]
    if TF_AVAILABLE:
        img_array = img_array.astype(np.float32) / 255.0
    return img_array

def tensor_to_image(tensor):
    if TF_AVAILABLE:
        tensor = tensor * 255
        tensor = np.array(tensor, dtype=np.uint8)
        if np.ndim(tensor) > 3:
            tensor = tensor[0]
    return Image.fromarray(tensor)

def create_style_pattern(style_type, size=512):
    img = np.zeros((size, size, 3), dtype=np.float32)
    if style_type == 'van_gogh':
        for i in range(size):
            for j in range(size):
                img[i, j] = [0.2 + 0.3 * np.sin(i * 0.05 + j * 0.03),
                             0.3 + 0.4 * np.cos(i * 0.03 + j * 0.05),
                             0.5 + 0.5 * np.sin(i * 0.04 + j * 0.04)]
    elif style_type == 'monet':
        for i in range(size):
            for j in range(size):
                img[i, j] = [0.4 + 0.3 * np.random.random(),
                             0.5 + 0.2 * np.random.random(),
                             0.6 + 0.3 * np.random.random()]
    elif style_type == 'picasso':
        for i in range(size):
            for j in range(size):
                img[i, j] = [0.7 if (i + j) % 40 < 20 else 0.3,
                             0.5 if i % 30 < 15 else 0.2,
                             0.4 if j % 25 < 12 else 0.6]
    else:
        for i in range(size):
            for j in range(size):
                img[i, j] = [0.5 + 0.5 * np.sin(i * 0.02),
                             0.5 + 0.5 * np.cos(j * 0.02),
                             0.5]
    return img[np.newaxis, ...]

def apply_style_transfer_fallback(content_image_path, style_type='van_gogh'):
    content_img = cv2.imread(content_image_path)
    if content_img is None:
        pil_img = Image.open(content_image_path).convert('RGB')
        pil_img = pil_img.resize((800, 600))
        content_img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
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
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        l = clahe.apply(l)
        styled = cv2.merge([l, a, b])
        styled = cv2.cvtColor(styled, cv2.COLOR_LAB2BGR)
    elif style_type == 'kandinsky':
        styled = cv2.pyrMeanShiftFiltering(content_img, 21, 51)
        styled = cv2.detailEnhance(styled, sigma_s=10, sigma_r=0.5)

    styled_rgb = cv2.cvtColor(styled, cv2.COLOR_BGR2RGB)
    return Image.fromarray(styled_rgb)

def apply_neural_style_transfer_real(content_path, style_type='van_gogh'):
    if not TF_AVAILABLE or hub_model is None:
        return apply_style_transfer_fallback(content_path, style_type)
    try:
        import tensorflow as tf
        content_image = load_img(content_path)
        style_image = create_style_pattern(style_type)
        stylized_image = hub_model(tf.constant(content_image), tf.constant(style_image))[0]
        result = tensor_to_image(stylized_image.numpy())
        return result
    except Exception as e:
        print(f"Error in neural style transfer: {e}")
        return apply_style_transfer_fallback(content_path, style_type)
