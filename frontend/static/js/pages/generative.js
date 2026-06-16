var palettes = {
  'vibrant': ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8'],
  'pastel': ['#FFB3BA', '#BAFFC9', '#BAE1FF', '#FFFFBA', '#FFD9BA'],
  'neon': ['#FF10F0', '#00F0FF', '#FFFF00', '#FF1010', '#10FF10'],
  'earth': ['#8B4513', '#228B22', '#DEB887', '#6B8E23', '#CD853F'],
  'ocean': ['#006994', '#1E88E5', '#42A5F5', '#64B5F6', '#90CAF9'],
  'sunset': ['#FF6B35', '#F7931E', '#FDC830', '#F37335', '#C73E1D']
};

document.addEventListener('DOMContentLoaded', function () {
  var artType = document.getElementById('art_type');
  if (!artType) return;

  var geoControls = document.getElementById('geometric-controls');
  var fracControls = document.getElementById('fractal-controls');
  var spirControls = document.getElementById('spiral-controls');

  artType.addEventListener('change', function () {
    geoControls.style.display = 'none';
    fracControls.style.display = 'none';
    spirControls.style.display = 'none';

    if (this.value === 'geometric') geoControls.style.display = 'block';
    else if (this.value === 'fractal') fracControls.style.display = 'block';
    else if (this.value === 'spiral') spirControls.style.display = 'block';
  });

  function syncSlider(sliderId, numId, displayId) {
    var slider = document.getElementById(sliderId);
    var num = document.getElementById(numId);
    var display = document.getElementById(displayId);
    if (!slider || !num) return;

    slider.addEventListener('input', function () {
      num.value = this.value;
      if (display) display.textContent = this.value;
    });
    num.addEventListener('input', function () {
      slider.value = this.value;
      if (display) display.textContent = this.value;
    });
  }

  syncSlider('num_shapes', 'num_shapes_exact', 'numValue');
  syncSlider('depth', 'depth_exact', 'depthValue');
  syncSlider('density', 'density_exact', 'densityValue');

  var paletteSelect = document.getElementById('palette');
  if (paletteSelect) {
    paletteSelect.addEventListener('change', updatePalettePreview);
    updatePalettePreview();
  }

  artType.dispatchEvent(new Event('change'));
});

function updatePalettePreview() {
  var select = document.getElementById('palette');
  if (!select) return;
  var colors = palettes[select.value];
  var preview = document.getElementById('palette-preview');
  if (!preview) return;

  preview.innerHTML = '';
  colors.forEach(function (color) {
    var div = document.createElement('div');
    div.style.backgroundColor = color;
    div.title = color;
    preview.appendChild(div);
  });
}

function shareImage() {
  showToast('📋 Link copied to clipboard! (Share feature)');
}
