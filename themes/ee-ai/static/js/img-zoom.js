// Click-to-expand spot illustrations.
// The small floated woodcuts (.img-right / .img-left) grow to full column width
// in place when clicked. A discreet footer toggle flips them all at once and
// remembers the choice across pages. Progressive enhancement: without this file
// the images stay as plain small floats.
(function () {
  "use strict";

  var KEY = "ee-img-expanded";
  var imgs = document.querySelectorAll(".prose img.img-right, .prose img.img-left");
  if (!imgs.length) return;

  var expandAll = false;
  try { expandAll = localStorage.getItem(KEY) === "1"; } catch (e) {}

  function setExpanded(img, on) {
    img.classList.toggle("is-expanded", on);
    img.setAttribute("aria-expanded", on ? "true" : "false");
  }

  imgs.forEach(function (img) {
    img.classList.add("is-zoomable");
    img.setAttribute("role", "button");
    img.setAttribute("tabindex", "0");
    var label = img.getAttribute("alt") || "image";
    img.setAttribute("aria-label", "Expand or shrink: " + label);
    setExpanded(img, expandAll);

    img.addEventListener("click", function () {
      setExpanded(img, !img.classList.contains("is-expanded"));
    });
    img.addEventListener("keydown", function (e) {
      if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        setExpanded(img, !img.classList.contains("is-expanded"));
      }
    });
  });

  var toggle = document.querySelector(".img-zoom-toggle");
  if (!toggle) return;

  var stateEl = toggle.querySelector(".iz-state");
  function reflect(on) {
    toggle.setAttribute("aria-pressed", on ? "true" : "false");
    if (stateEl) stateEl.textContent = on ? "large" : "small";
  }

  toggle.hidden = false;
  reflect(expandAll);

  toggle.addEventListener("click", function () {
    expandAll = !expandAll;
    try { localStorage.setItem(KEY, expandAll ? "1" : "0"); } catch (e) {}
    imgs.forEach(function (img) { setExpanded(img, expandAll); });
    reflect(expandAll);
  });
})();
