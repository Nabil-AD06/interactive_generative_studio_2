import random
import numpy as np
import cv2
from PIL import Image, ImageFilter, ImageEnhance, ImageOps

def apply_image_filter(image_path, filter_type):
    img = Image.open(image_path)
    img = img.resize((800, 600))

    if filter_type == 'grayscale':
        img = ImageOps.grayscale(img).convert('RGB')
    elif filter_type == 'sepia':
        grayscale = ImageOps.grayscale(img)
        sepia = Image.new('RGB', img.size)
        pixels = sepia.load()
        gray_pixels = grayscale.load()
        for i in range(img.size[0]):
            for j in range(img.size[1]):
                g = gray_pixels[i, j]
                pixels[i, j] = (min(255, int(g)), min(255, int(g * 0.95)), min(255, int(g * 0.82)))
        img = sepia
    elif filter_type == 'neon':
        img = ImageEnhance.Color(img).enhance(3.0)
        img = ImageEnhance.Brightness(img).enhance(1.2)
        img = ImageEnhance.Contrast(img).enhance(1.5)
    elif filter_type == 'invert':
        img = ImageOps.invert(img.convert('RGB'))
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
    elif filter_type == 'rotate_90':
        img = img.rotate(90, expand=True)
    elif filter_type == 'rotate_180':
        img = img.rotate(180)
    elif filter_type == 'flip_horizontal':
        img = ImageOps.mirror(img)
    elif filter_type == 'flip_vertical':
        img = ImageOps.flip(img)
    elif filter_type == 'vintage':
        img = apply_vintage_effect(img)
    elif filter_type == 'warm':
        img = apply_temperature_effect(img, warm=True)
    elif filter_type == 'cool':
        img = apply_temperature_effect(img, warm=False)
    elif filter_type == 'high_contrast':
        img = ImageEnhance.Contrast(img).enhance(2.0)

    return img

def apply_glitch_effect(img):
    arr = np.array(img)
    h, w = arr.shape[:2]
    for _ in range(10):
        y = random.randint(0, h - 20)
        shift = random.randint(-50, 50)
        if shift > 0:
            arr[y:y + 20, shift:] = arr[y:y + 20, :-shift]
        elif shift < 0:
            arr[y:y + 20, :shift] = arr[y:y + 20, -shift:]
    if len(arr.shape) == 3:
        s = random.randint(5, 15)
        arr[:, s:, 0] = arr[:, :-s, 0]
        arr[:, :-s, 2] = arr[:, s:, 2]
    return Image.fromarray(arr)

def apply_watercolor_effect(img):
    cv_img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    cv_img = cv2.bilateralFilter(cv_img, 9, 75, 75)
    cv_img = cv2.medianBlur(cv_img, 5)
    cv_img = cv2.pyrMeanShiftFiltering(cv_img, 21, 51)
    return Image.fromarray(cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB))

def apply_oil_painting_effect(img):
    cv_img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    for _ in range(3):
        cv_img = cv2.bilateralFilter(cv_img, 9, 100, 100)
    return Image.fromarray(cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB))

def apply_cartoon_effect(img):
    cv_img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)
    edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
    color = cv2.bilateralFilter(cv_img, 9, 250, 250)
    cartoon = cv2.bitwise_and(color, color, mask=edges)
    return Image.fromarray(cv2.cvtColor(cartoon, cv2.COLOR_BGR2RGB))

def apply_sketch_effect(img):
    cv_img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
    inverted = 255 - gray
    blurred = cv2.GaussianBlur(inverted, (21, 21), 0)
    inverted_blur = 255 - blurred
    sketch = cv2.divide(gray, inverted_blur, scale=256.0)
    return Image.fromarray(cv2.cvtColor(sketch, cv2.COLOR_GRAY2RGB))

def apply_vintage_effect(img):
    grayscale = ImageOps.grayscale(img)
    sepia = Image.new('RGB', img.size)
    pixels = sepia.load()
    gray_pixels = grayscale.load()
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            g = gray_pixels[i, j]
            pixels[i, j] = (min(255, int(g * 1.1)), min(255, int(g * 0.9)), min(255, int(g * 0.7)))
    sepia = ImageEnhance.Contrast(sepia).enhance(0.8)
    sepia = sepia.filter(ImageFilter.GaussianBlur(radius=1))
    return sepia

def apply_temperature_effect(img, warm=True):
    arr = np.array(img, dtype=np.float32)
    if warm:
        arr[:, :, 0] = np.clip(arr[:, :, 0] * 1.1, 0, 255)
        arr[:, :, 2] = np.clip(arr[:, :, 2] * 0.9, 0, 255)
    else:
        arr[:, :, 0] = np.clip(arr[:, :, 0] * 0.9, 0, 255)
        arr[:, :, 2] = np.clip(arr[:, :, 2] * 1.1, 0, 255)
    return Image.fromarray(arr.astype(np.uint8))
