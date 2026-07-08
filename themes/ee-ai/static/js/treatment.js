// Scroll-effects ("fx") runtime for pages that opt into a treatment (body.treat-*).
// Treatment-agnostic: it reads the .fx-act markers and the .fx-stage [data-depth]
// layers and drives three things - the act state (body[data-act], which the CSS
// hangs the palette on), parallax on the layers, and a 0..1 scroll-progress custom
// prop for gradient blending. All palette/art specifics live in style.css; this
// file only moves numbers. Progressive enhancement: without it the page just sits
// at act 0 with static layers.
(function () {
  "use strict";

  var body = document.body;
  if (!body || body.dataset.fxReady) return;

  var stage = document.querySelector(".fx-stage");
  var markers = document.querySelectorAll(".fx-act");
  var layers = stage ? stage.querySelectorAll("[data-depth]") : [];
  // nothing to drive? bail (e.g. the class is present but there is no stage/markers)
  if (!markers.length && !layers.length) return;
  body.dataset.fxReady = "1";

  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var article = document.querySelector("article") || document.getElementById("content");

  // ---- act watcher: latest marker whose top has crossed the viewport midline ----
  // Runs in BOTH motion modes; palette swaps just become instant under reduced
  // motion because the global rule at style.css:636 already kills transitions.
  function updateAct() {
    var mid = window.innerHeight / 2;
    var act = "0";
    for (var i = 0; i < markers.length; i++) {
      if (markers[i].getBoundingClientRect().top <= mid) act = markers[i].dataset.act;
    }
    if (body.dataset.act !== act) body.dataset.act = act;
  }

  // ---- progress: 0..1 across the article's scroll range, for gradient blending ----
  // Returns the clamped value so the same number can drive progress-anchored layers.
  function updateProgress() {
    if (!article) return 0;
    var rect = article.getBoundingClientRect();
    var range = rect.height - window.innerHeight;
    var p = range > 0 ? -rect.top / range : 0;
    p = Math.max(0, Math.min(1, p));
    body.style.setProperty("--fx-progress", p.toFixed(4));
    return p;
  }

  // ---- parallax: shift each depth layer by -(scrollY * depth) (motion only) ----
  function updateParallax(y, p) {
    for (var i = 0; i < layers.length; i++) {
      var layer = layers[i];
      // A layer marked data-anchor="descend" ignores scroll-speed parallax and
      // instead travels from its CSS start position down to the bottom of the
      // viewport across the whole article, landing flush at the bottom exactly at
      // the end (p === 1). offsetTop is its start (its resolved CSS top in px),
      // offsetHeight its rendered height - so it is length- and viewport-agnostic.
      if (layer.dataset.anchor === "descend") {
        var travel = (window.innerHeight - layer.offsetHeight) - layer.offsetTop;
        layer.style.transform = "translate3d(0, " + ((p || 0) * travel).toFixed(2) + "px, 0)";
        continue;
      }
      var d = parseFloat(layer.dataset.depth) || 0;
      layer.style.transform = "translate3d(0, " + (-(y * d)).toFixed(2) + "px, 0)";
    }
  }

  if (reduce) {
    // Reduced motion: no rAF loop, no transforms on layers. Act flips and progress
    // still run so the palette (which has no transition here) stays correct.
    var onScrollReduced = function () { updateAct(); updateProgress(); };
    window.addEventListener("scroll", onScrollReduced, { passive: true });
    window.addEventListener("resize", onScrollReduced, { passive: true });
    onScrollReduced();
  } else {
    var ticking = false;
    var onScroll = function () {
      if (ticking) return;
      ticking = true;
      window.requestAnimationFrame(function () {
        updateAct();
        var p = updateProgress();
        updateParallax(window.scrollY || window.pageYOffset, p);
        ticking = false;
      });
    };
    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", onScroll, { passive: true });
    onScroll();
  }
})();
