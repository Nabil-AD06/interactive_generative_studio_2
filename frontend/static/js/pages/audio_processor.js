document.addEventListener('DOMContentLoaded', function () {
  var durationInput = document.getElementById('duration');
  if (durationInput) {
    var display = document.createElement('span');
    display.className = 'value-display';
    display.style.marginLeft = '0.5rem';
    display.textContent = durationInput.value + 's';
    durationInput.parentNode.appendChild(display);

    durationInput.addEventListener('input', function () {
      display.textContent = this.value + 's';
    });
  }
});
