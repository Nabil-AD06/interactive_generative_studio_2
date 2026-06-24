document.addEventListener('DOMContentLoaded', function () {
  setCurrentYear();
  updateBreadcrumbs();
  setActiveNav();
  createParticles();
  addFadeInAnimation();

  setTimeout(function () {
    showStatus('\u{1F4A1} Press ? for keyboard shortcuts', 'info');
  }, 2000);

  initNavToggle();
  initThemeToggle();
  initKeyboardShortcuts();
  initFileDragDrop();
  initFormSubmit();
  initAutoSave();
});

function setCurrentYear() {
  var el = document.getElementById('currentYear');
  if (el) el.textContent = new Date().getFullYear();
}

function updateBreadcrumbs() {
  var path = window.location.pathname;
  var pageName = {
    '/': 'Home',
    '/generative': 'Generative Art',
    '/data-viz': 'Data Visualization',
    '/image-processor': 'Image Processing',
    '/audio-processor': 'Audio Processing',
    '/style-transfer': 'Style Transfer',
    '/gallery': 'Gallery'
  };
  var el = document.getElementById('currentPage');
  if (el) el.textContent = pageName[path] || 'Dashboard';
}

function setActiveNav() {
  var path = window.location.pathname;
  document.querySelectorAll('nav a').forEach(function (a) {
    var href = a.getAttribute('href');
    if (href === path || (path !== '/' && href !== '/' && path.startsWith(href))) {
      a.classList.add('active');
    } else if (path === '/' && href === '/') {
      a.classList.add('active');
    }
  });
}

function scrollToTop() {
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

function toggleHelp() {
  document.getElementById('helpOverlay').classList.toggle('active');
}

function showStatus(message, type) {
  var indicator = document.getElementById('statusIndicator');
  var icon = indicator.querySelector('.status-icon');
  var text = indicator.querySelector('.status-text');

  indicator.className = 'status-indicator';

  if (type === 'error') {
    indicator.classList.add('error');
    icon.textContent = '\u274C';
  } else if (type === 'warning') {
    indicator.classList.add('warning');
    icon.textContent = '\u26A0\uFE0F';
  } else {
    icon.textContent = '\u2705';
  }

  text.textContent = message;
  indicator.classList.add('active');

  clearTimeout(indicator._timeout);
  indicator._timeout = setTimeout(function () {
    indicator.classList.remove('active');
  }, 3000);
}

function showToast(message, duration) {
  duration = duration || 3000;
  var toast = document.getElementById('toast');
  toast.textContent = message;
  toast.classList.add('show');
  setTimeout(function () {
    toast.classList.remove('show');
  }, duration);
}

function createConfetti() {
  var colors = ['#10b981', '#0d9488', '#f59e0b', '#34d399', '#ef4444'];
  for (var i = 0; i < 50; i++) {
    var confetti = document.createElement('div');
    confetti.style.cssText =
      'position:fixed;width:10px;height:10px;background-color:' +
      colors[Math.floor(Math.random() * colors.length)] +
      ';left:' + Math.random() * window.innerWidth + 'px;top:-10px;border-radius:50%;z-index:10000;pointer-events:none;';
    document.body.appendChild(confetti);

    var anim = confetti.animate([
      { transform: 'translateY(0) rotate(0deg)', opacity: 1 },
      { transform: 'translateY(' + window.innerHeight + 'px) rotate(720deg)', opacity: 0 }
    ], {
      duration: 3000 + Math.random() * 2000,
      easing: 'cubic-bezier(0.25, 0.46, 0.45, 0.94)'
    });
    anim.onfinish = function () { confetti.remove(); };
  }
}

function createParticles() {
  var container = document.getElementById('particles');
  if (!container) return;
  for (var i = 0; i < 25; i++) {
    var p = document.createElement('div');
    p.className = 'particle';
    p.style.left = Math.random() * 100 + '%';
    p.style.top = Math.random() * 100 + '%';
    p.style.animationDelay = Math.random() * 20 + 's';
    p.style.animationDuration = (15 + Math.random() * 15) + 's';
    container.appendChild(p);
  }
}

function addFadeInAnimation() {
  var elements = document.querySelectorAll('.feature-card, .control-panel, .image-box, .audio-box');
  var observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) entry.target.classList.add('fade-in');
    });
  }, { threshold: 0.1 });
  elements.forEach(function (el) { observer.observe(el); });
}

function initNavToggle() {
  var toggle = document.getElementById('navToggle');
  var navUl = document.querySelector('nav ul');
  if (!toggle || !navUl) return;

  toggle.addEventListener('click', function () {
    this.classList.toggle('active');
    navUl.classList.toggle('open');
  });

  document.querySelectorAll('nav a').forEach(function (link) {
    link.addEventListener('click', function () {
      toggle.classList.remove('active');
      navUl.classList.remove('open');
    });
  });
}

function initThemeToggle() {
  var toggle = document.getElementById('themeToggle');
  if (!toggle) return;
  var isDark = localStorage.getItem('theme') === 'dark';

  function applyTheme(dark) {
    isDark = dark;
    document.documentElement.setAttribute('data-theme', dark ? 'dark' : 'light');
    toggle.textContent = dark ? '\u2600\uFE0F' : '\uD83C\uDF19';
    localStorage.setItem('theme', dark ? 'dark' : 'light');
    if (dark) {
      document.body.style.background = '';
    } else {
      document.body.style.background = '';
    }
  }

  applyTheme(isDark);
  toggle.addEventListener('click', function () { applyTheme(!isDark); });
}

function initKeyboardShortcuts() {
  var konamiCode = [];
  var konamiPattern = ['ArrowUp', 'ArrowUp', 'ArrowDown', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'ArrowLeft', 'ArrowRight', 'b', 'a'];

  document.addEventListener('keydown', function (e) {
    if (e.ctrlKey && e.key === 'h') { e.preventDefault(); window.location.href = '/'; }
    if (e.ctrlKey && e.key === 'g') { e.preventDefault(); window.location.href = '/gallery'; }
    if (e.key === 'Escape') {
      var help = document.getElementById('helpOverlay');
      if (help) help.classList.remove('active');
      var navUl = document.querySelector('nav ul');
      var toggle = document.getElementById('navToggle');
      if (navUl && toggle) { navUl.classList.remove('open'); toggle.classList.remove('active'); }
    }
    if (e.key === '?' && !e.ctrlKey && !e.altKey) { e.preventDefault(); toggleHelp(); }
    if (e.ctrlKey && e.key === 'Enter') {
      var form = document.querySelector('form');
      if (form) form.submit();
    }
    if (e.altKey && e.key === 'ArrowLeft') { e.preventDefault(); window.history.back(); }

    konamiCode.push(e.key);
    konamiCode = konamiCode.slice(-10);
    if (konamiCode.join('') === konamiPattern.join('')) {
      showToast('\u{1F389} SECRET UNLOCKED! Rainbow Mode!', 5000);
      document.body.style.animation = 'rainbow 3s linear infinite';
    }
  });
}

function initFileDragDrop() {
  document.querySelectorAll('.file-drop-zone input[type="file"], .input-wrapper input[type="file"]').forEach(function (input) {
    var parent = input.closest('.file-drop-zone') || input.parentElement;

    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(function (name) {
      parent.addEventListener(name, function (e) {
        e.preventDefault();
        e.stopPropagation();
      }, false);
    });

    ['dragenter', 'dragover'].forEach(function (name) {
      parent.addEventListener(name, function () { parent.classList.add('dragover'); }, false);
    });

    ['dragleave', 'drop'].forEach(function (name) {
      parent.addEventListener(name, function () { parent.classList.remove('dragover'); }, false);
    });

    parent.addEventListener('drop', function (e) {
      input.files = e.dataTransfer.files;
      showStatus('File ready to upload!');
    }, false);
  });
}

function initFormSubmit() {
  document.querySelectorAll('form').forEach(function (form) {
    form.addEventListener('submit', function () {
      var btn = form.querySelector('button[type="submit"], .btn[type="submit"]');
      if (btn) {
        btn.disabled = true;
        btn.innerHTML = '\u23F3 Processing...';
        btn.classList.add('loading');
      }
      showStatus('Processing your request...', 'warning');
    });
  });
}

function initAutoSave() {
  document.querySelectorAll('input[type="range"], input[type="number"]').forEach(function (input) {
    var saved = localStorage.getItem('form_' + input.name);
    if (saved) input.value = saved;
    input.addEventListener('change', function () {
      localStorage.setItem('form_' + input.name, this.value);
    });
  });
}

document.addEventListener('DOMContentLoaded', function () {
  if (document.querySelector('.image-container img')) {
    setTimeout(createConfetti, 500);
  }
});
