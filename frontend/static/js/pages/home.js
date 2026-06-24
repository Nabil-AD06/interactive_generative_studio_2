document.addEventListener('DOMContentLoaded', function () {
  var cards = document.querySelectorAll('.feature-card');
  cards.forEach(function (card, index) {
    card.style.animationDelay = (index * 0.1) + 's';
  });
});
