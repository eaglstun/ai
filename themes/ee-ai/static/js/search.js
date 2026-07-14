// Seeded semantic search. Runs entirely in the browser, no server, no vector database.
//
// The trick, and its honest limit: Hamming distance needs the query as BITS, and the
// only thing that turns arbitrary text into those bits is the embedding model - which
// lives in Ollama on a laptop, not in your browser. So typing does not produce a
// vector. Instead:
//
//   1. SEED.   A cheap lexical pass over titles/tags/summaries finds the page closest
//              to what you typed. This is a page-finder, not the search.
//   2. EXPAND. Everything after that is pure semantic ID: XOR the seed's ID against
//              every other page's, popcount the difference, sort ascending. That's how
//              a search for "quantization" surfaces pages that never say the word.
//
// Paste a raw 32-character ID into the box and step 1 is skipped entirely - it seeds
// straight from the bits.
(function () {
  var input = document.getElementById('site-search-input');
  if (!input) return;

  var resultsEl = document.getElementById('search-results');
  var statusEl = document.getElementById('search-status');

  // Must match scripts/semantic-ids.py exactly. If these drift, the distances are junk.
  var ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_';
  var SEMANTIC_BITS = 172;
  var TAIL_BITS = 20; // 16-bit day + 4-bit tiebreak: noise, masked off before comparing
  var MAX_DISTANCE = 72; // ~5th percentile of random pairs; past this you rank noise
  var NEIGHBOUR_COUNT = 6;
  var ID_RE = /^[A-Za-z0-9_-]{32}$/;

  var pages = null;
  var loading = null;

  // 32 base64url chars -> 24 bytes. Note there is no dash-stripping: `-` is a real
  // character in the alphabet, and treating it as a separator would silently corrupt
  // every comparison.
  function decode(id) {
    var bytes = new Uint8Array(24);
    var acc = 0;
    var bits = 0;
    var out = 0;
    for (var i = 0; i < id.length; i++) {
      var v = ALPHABET.indexOf(id.charAt(i));
      if (v < 0) return null;
      acc = (acc << 6) | v;
      bits += 6;
      while (bits >= 8) {
        bits -= 8;
        bytes[out++] = (acc >> bits) & 0xff;
      }
    }
    return out === 24 ? bytes : null;
  }

  // The bottom 20 bits are a date and a tiebreak hash - pure noise to a distance
  // function. 192 - 20 = 172 semantic bits: bytes 0..20 whole, plus the top 4 bits of
  // byte 21. Compare without this mask and two identical pages published a year apart
  // look unrelated.
  var FULL_BYTES = (SEMANTIC_BITS - (SEMANTIC_BITS % 8)) / 8; // 21
  var PARTIAL_MASK = 0xff << (8 - (SEMANTIC_BITS % 8)) & 0xff; // 0xf0

  function popcount(b) {
    b = b - ((b >> 1) & 0x55);
    b = (b & 0x33) + ((b >> 2) & 0x33);
    return (b + (b >> 4)) & 0x0f;
  }

  function hamming(a, b) {
    var d = 0;
    for (var i = 0; i < FULL_BYTES; i++) d += popcount(a[i] ^ b[i]);
    d += popcount((a[FULL_BYTES] ^ b[FULL_BYTES]) & PARTIAL_MASK);
    return d;
  }

  // ---- step 1: the seed (lexical, and deliberately dumb) ----
  function lexicalScore(page, tokens) {
    var title = page.t.toLowerCase();
    var summary = (page.s || '').toLowerCase();
    var tags = (page.g || []).join(' ').toLowerCase();
    var score = 0;

    for (var i = 0; i < tokens.length; i++) {
      var tok = tokens[i];
      var hit = 0;
      if (title.indexOf(tok) !== -1) hit += title === tok ? 24 : 10;
      if (tags.indexOf(tok) !== -1) hit += 6;
      if (summary.indexOf(tok) !== -1) hit += 3;
      if (hit === 0) return 0; // every word must land somewhere. AND, not OR.
      score += hit;
    }
    return score;
  }

  function esc(s) {
    return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  function kindLabel(k) {
    if (!k) return 'Page';
    if (k === 'glossary') return 'Glossary';
    if (k === 'deep-dives') return 'Deep dive';
    return k.charAt(0).toUpperCase() + k.slice(1);
  }

  function card(page, distance) {
    return '<li><a href="' + esc(page.u) + '">' +
      '<span class="related-kind">' + esc(kindLabel(page.k)) +
      (distance == null ? '' : '<span class="search-dist">' + distance + ' bits</span>') +
      '</span>' +
      '<span class="related-title">' + esc(page.t) + '</span>' +
      (page.s ? '<span class="related-summary">' + esc(page.s) + '</span>' : '') +
      '</a></li>';
  }

  function section(heading, items) {
    return '<section class="search-group"><h2>' + heading + '</h2>' +
      '<ul class="related-list">' + items.join('') + '</ul></section>';
  }

  function render(query) {
    var q = query.trim();
    if (!q) {
      resultsEl.innerHTML = '';
      statusEl.hidden = true;
      return;
    }

    var seedBits = null;
    var seedPage = null;
    var matches = [];

    if (ID_RE.test(q) && decode(q)) {
      // Someone pasted an ID. Skip the seed hunt and go straight to the bits.
      seedBits = decode(q);
      for (var i = 0; i < pages.length; i++) {
        if (pages[i].x === q) seedPage = pages[i];
      }
    } else {
      var tokens = q.toLowerCase().split(/\s+/).filter(Boolean);
      for (var j = 0; j < pages.length; j++) {
        var s = lexicalScore(pages[j], tokens);
        if (s > 0) matches.push({ page: pages[j], score: s });
      }
      matches.sort(function (a, b) { return b.score - a.score; });
      if (matches.length) {
        seedPage = matches[0].page;
        seedBits = decode(seedPage.x);
      }
    }

    if (!seedBits) {
      statusEl.hidden = false;
      statusEl.textContent = 'Nothing matched "' + q + '". The seed pass is a plain ' +
        'substring match over titles, tags, and summaries - it has to land on one page ' +
        'before the bits can take over.';
      resultsEl.innerHTML = '';
      return;
    }

    // ---- step 2: expand by Hamming distance. This is the actual search. ----
    var seen = {};
    for (var m = 0; m < matches.length; m++) seen[matches[m].page.u] = true;

    var near = [];
    for (var k = 0; k < pages.length; k++) {
      var p = pages[k];
      if (seen[p.u]) continue;
      if (seedPage && p.u === seedPage.u) continue;
      var bits = decode(p.x);
      if (!bits) continue;
      var d = hamming(seedBits, bits);
      if (d <= MAX_DISTANCE) near.push({ page: p, d: d });
    }
    near.sort(function (a, b) { return a.d - b.d; });
    near = near.slice(0, NEIGHBOUR_COUNT);

    var html = '';
    if (matches.length) {
      html += section('Matches', matches.map(function (m) { return card(m.page, null); }));
    } else if (seedPage) {
      html += section('That ID', [card(seedPage, 0)]);
    }
    if (near.length) {
      var label = seedPage
        ? 'Near <em>' + esc(seedPage.t) + '</em> in meaning'
        : 'Near that ID in meaning';
      html += section(label, near.map(function (n) { return card(n.page, n.d); }));
    }

    resultsEl.innerHTML = html;
    statusEl.hidden = false;
    statusEl.textContent = matches.length
      ? matches.length + (matches.length === 1 ? ' match' : ' matches') +
        (near.length ? ', plus ' + near.length + ' near it in meaning.' : '.')
      : 'Seeded straight from the bits.';
  }

  function load() {
    if (loading) return loading;
    loading = fetch('/index.json')
      .then(function (r) {
        if (!r.ok) throw new Error(r.status);
        return r.json();
      })
      .then(function (data) { pages = data; })
      .catch(function () {
        statusEl.hidden = false;
        statusEl.textContent = 'The search index failed to load.';
      });
    return loading;
  }

  function onInput() {
    var q = input.value;
    load().then(function () {
      if (pages && input.value === q) render(q);
    });
  }

  input.addEventListener('input', onInput);

  // Deep links: /search/?q=gguf - same convention as the glossary filter.
  var initial = new URLSearchParams(window.location.search).get('q');
  if (initial) {
    input.value = initial;
    onInput();
  } else {
    load();
  }
})();
