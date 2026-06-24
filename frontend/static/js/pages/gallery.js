document.addEventListener('DOMContentLoaded', function () {
  var filterButtons = document.querySelectorAll('.filter-btn');
  filterButtons.forEach(function (btn) {
    btn.addEventListener('click', function () {
      filterButtons.forEach(function (b) { b.classList.remove('active'); });
      this.classList.add('active');

      var filter = this.getAttribute('data-filter');
      document.querySelectorAll('.thumbnail-card').forEach(function (card) {
        if (filter === 'all' || card.getAttribute('data-type') === filter) {
          card.style.display = '';
        } else {
          card.style.display = 'none';
        }
      });
    });
  });
});
