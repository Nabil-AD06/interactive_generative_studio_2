import random
import math
from PIL import Image, ImageDraw
from shapes import Circle, Square, Triangle

def get_color_palette(palette_name):
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

def generate_fractal_tree(depth):
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
        s = 3 + (i % 50) // 10
        draw.ellipse([x - s, y - s, x + s, y + s], fill=color)
    return img
