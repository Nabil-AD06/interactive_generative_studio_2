document.addEventListener('DOMContentLoaded', function () {
  var fileInput = document.getElementById('image');
  if (!fileInput) return;

  fileInput.addEventListener('change', function () {
    if (this.files && this.files[0]) {
      var reader = new FileReader();
      reader.onload = function (e) {
        var preview = document.getElementById('upload-preview');
        if (!preview) {
          preview = document.createElement('div');
          preview.id = 'upload-preview';
          preview.style.cssText = 'margin-top:1rem;text-align:center;';
          fileInput.parentNode.appendChild(preview);
        }
        preview.innerHTML = '<img src="' + e.target.result + '" style="max-height:200px;border-radius:10px;box-shadow:0 4px 15px rgba(0,0,0,0.1);">';
      };
      reader.readAsDataURL(this.files[0]);
    }
  });
});
