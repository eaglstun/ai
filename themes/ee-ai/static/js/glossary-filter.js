// Live client-side filter for the glossary index. Progressive enhancement:
// without JS, every term is visible and the search box does nothing harmful.
(function () {
  var input = document.getElementById('glossary-search');
  if (!input) return;

  var cards = Array.prototype.slice.call(document.querySelectorAll('.term-card'));
  var groups = Array.prototype.slice.call(document.querySelectorAll('.glossary-group'));
  var emptyNote = document.getElementById('filter-empty');

  function apply() {
    var q = input.value.trim().toLowerCase();
    var anyVisible = false;

    cards.forEach(function (card) {
      var hay = card.getAttribute('data-term') + ' ' + card.getAttribute('data-summary');
      var match = q === '' || hay.indexOf(q) !== -1;
      card.hidden = !match;
      if (match) anyVisible = true;
    });

    // Hide a category heading when all of its cards are filtered out.
    groups.forEach(function (group) {
      var visible = group.querySelectorAll('.term-card:not([hidden])').length;
      group.hidden = visible === 0;
    });

    if (emptyNote) emptyNote.hidden = anyVisible;
  }

  input.addEventListener('input', apply);

  // Support deep links like /glossary/?q=gguf
  var params = new URLSearchParams(window.location.search);
  var initial = params.get('q');
  if (initial) {
    input.value = initial;
    apply();
  }
})();
