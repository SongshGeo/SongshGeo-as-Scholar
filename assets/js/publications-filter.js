/* publications-filter.js
 *
 * Enhances the home `#featured` (Publications) Isotope grid with:
 *   - a clickable year timeline in col-lg-4 (multi-select)
 *   - a keyword chip cloud in col-lg-8 (multi-select, ANY-match)
 *   - role filter buttons rewired to combine with the above filters
 *
 * Hooks the existing Isotope instance via `Isotope.data()` after
 * Hugo Blox finishes initializing it.
 */
(function () {
  'use strict';

  var SECTION_ID = 'featured';
  var POLL_INTERVAL_MS = 100;
  var MAX_POLL_MS = 8000;

  if (document.readyState !== 'loading') {
    init();
  } else {
    document.addEventListener('DOMContentLoaded', init);
  }

  function init() {
    var section = document.getElementById(SECTION_ID);
    if (!section) return;
    var container = section.querySelector('.projects-container');
    if (!container) return;

    waitForIsotope(container, function (iso) {
      buildUI(section, container, iso);
    });
  }

  function waitForIsotope(elem, cb) {
    var elapsed = 0;
    function poll() {
      var iso = (typeof Isotope !== 'undefined' && Isotope.data) ? Isotope.data(elem) : null;
      if (iso) return cb(iso);
      elapsed += POLL_INTERVAL_MS;
      if (elapsed >= MAX_POLL_MS) {
        console.warn('[publications-filter] Isotope not ready after ' + MAX_POLL_MS + 'ms');
        return;
      }
      setTimeout(poll, POLL_INTERVAL_MS);
    }
    poll();
  }

  function buildUI(section, container, iso) {
    var items = Array.prototype.slice.call(container.querySelectorAll('.isotope-item'));
    var meta = items.map(extractMeta);

    var allYears = uniq(meta.map(function (m) { return m.year; }).filter(Boolean)).sort().reverse();
    var allKeywords = uniq([].concat.apply([], meta.map(function (m) { return m.keywords; }))).sort();

    var state = {
      role: '*',                 // single-select (one of the role filter buttons)
      years: Object.create(null),// set-like, multi-select
      yearsCount: 0,
      keywords: Object.create(null),
      keywordsCount: 0,
    };

    // ---- Timeline (col-lg-4) ----
    var headingCol =
      section.querySelector('.section-heading.col-lg-4') ||
      section.querySelector('.col-lg-4.section-heading') ||
      section.querySelector('.section-heading');
    if (headingCol && allYears.length) {
      var timeline = buildTimeline(allYears, state, applyFilter);
      headingCol.appendChild(timeline);
    }

    // ---- Keyword chip cloud (col-lg-8) ----
    var itemsCol = section.querySelector('.col-lg-8') || container.parentNode;
    var toolbar = section.querySelector('.project-toolbar');
    if (itemsCol && allKeywords.length) {
      var picker = buildKeywordPicker(allKeywords, state, applyFilter);
      if (toolbar && toolbar.parentNode) {
        toolbar.parentNode.insertBefore(picker, toolbar.nextSibling);
      } else {
        itemsCol.insertBefore(picker, itemsCol.firstChild);
      }
    }

    // ---- Rewire role filter buttons ----
    var roleButtons = Array.prototype.slice.call(section.querySelectorAll('.project-filters a'));
    roleButtons.forEach(function (btn) {
      // Replace node to remove Hugo Blox's existing listeners
      var clone = btn.cloneNode(true);
      btn.parentNode.replaceChild(clone, btn);
      clone.addEventListener('click', function (e) {
        e.preventDefault();
        state.role = clone.getAttribute('data-filter') || '*';
        roleButtons.forEach(function (b) { b.classList.remove('active'); });
        // re-query (clones replaced originals)
        section.querySelectorAll('.project-filters a').forEach(function (b) {
          b.classList.toggle('active', b === clone);
        });
        applyFilter();
      });
    });
    // refresh roleButtons after replacement so future iterations work
    roleButtons = Array.prototype.slice.call(section.querySelectorAll('.project-filters a'));

    function applyFilter() {
      iso.arrange({
        // Isotope v3 (pkgd build) routes the filter function through
        // jQuery's `.is(fn)`, which calls fn as `fn.call(elem, index)`.
        // So the actual element is `this`, not the first argument.
        filter: function () {
          var elem = this;
          if (!elem || !elem.classList) return false;
          var m = extractMeta(elem);

          if (state.role && state.role !== '*') {
            var want = state.role.replace(/^\.js-id-/, '');
            if (m.tags.indexOf(want) === -1) return false;
          }

          if (state.yearsCount > 0 && !state.years[m.year]) return false;

          if (state.keywordsCount > 0) {
            var any = false;
            for (var i = 0; i < m.keywords.length; i++) {
              if (state.keywords[m.keywords[i]]) { any = true; break; }
            }
            if (!any) return false;
          }
          return true;
        },
      });
    }
  }

  // ---------- helpers ----------

  function extractMeta(elem) {
    var classes = (elem.className || '').split(/\s+/);
    var tags = [], keywords = [], year = null;
    for (var i = 0; i < classes.length; i++) {
      var c = classes[i];
      if (c.indexOf('js-id-') !== 0) continue;
      var name = c.slice(6);
      tags.push(name);
      var m = name.match(/^year-(\d{4})$/);
      if (m) {
        year = m[1];
      } else if (name.indexOf('role-') !== 0) {
        keywords.push(name);
      }
    }
    return { tags: tags, year: year, keywords: keywords };
  }

  function uniq(arr) {
    var seen = Object.create(null), out = [];
    for (var i = 0; i < arr.length; i++) {
      if (!seen[arr[i]]) { seen[arr[i]] = 1; out.push(arr[i]); }
    }
    return out;
  }

  function el(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text != null) e.textContent = text;
    return e;
  }

  function buildTimeline(years, state, onChange) {
    var wrap = el('div', 'pub-timeline');
    var label = el('div', 'pub-timeline-label', 'Year');
    var clear = el('button', 'pub-timeline-clear', 'Clear');
    clear.type = 'button';
    clear.style.display = 'none';
    var head = el('div', 'pub-timeline-head');
    head.appendChild(label);
    head.appendChild(clear);
    wrap.appendChild(head);

    var list = el('div', 'pub-timeline-list');
    var chips = years.map(function (y) {
      var chip = el('button', 'pub-year-chip', y);
      chip.type = 'button';
      chip.dataset.year = y;
      chip.addEventListener('click', function () {
        if (state.years[y]) {
          delete state.years[y]; state.yearsCount--;
          chip.classList.remove('active');
        } else {
          state.years[y] = 1; state.yearsCount++;
          chip.classList.add('active');
        }
        clear.style.display = state.yearsCount ? 'inline-block' : 'none';
        onChange();
      });
      list.appendChild(chip);
      return chip;
    });
    wrap.appendChild(list);

    clear.addEventListener('click', function () {
      state.years = Object.create(null);
      state.yearsCount = 0;
      chips.forEach(function (c) { c.classList.remove('active'); });
      clear.style.display = 'none';
      onChange();
    });

    return wrap;
  }

  function buildKeywordPicker(keywords, state, onChange) {
    var wrap = el('div', 'pub-keywords');

    var bar = el('div', 'pub-keywords-bar');
    var toggle = el('button', 'pub-keywords-toggle');
    toggle.type = 'button';
    toggle.innerHTML = '<i class="fas fa-tags" aria-hidden="true"></i><span>Topics</span>';
    var count = el('span', 'pub-keywords-count');
    toggle.appendChild(count);
    var clear = el('button', 'pub-keywords-clear', 'Clear');
    clear.type = 'button';
    clear.style.display = 'none';
    bar.appendChild(toggle);
    bar.appendChild(clear);
    wrap.appendChild(bar);

    var cloud = el('div', 'pub-keyword-cloud');
    cloud.style.display = 'none';
    wrap.appendChild(cloud);

    var chips = keywords.map(function (kw) {
      var label = kw.replace(/-/g, ' ');
      var chip = el('button', 'pub-keyword-chip', label);
      chip.type = 'button';
      chip.dataset.keyword = kw;
      chip.addEventListener('click', function () {
        if (state.keywords[kw]) {
          delete state.keywords[kw]; state.keywordsCount--;
          chip.classList.remove('active');
        } else {
          state.keywords[kw] = 1; state.keywordsCount++;
          chip.classList.add('active');
        }
        renderCount();
        onChange();
      });
      cloud.appendChild(chip);
      return chip;
    });

    function renderCount() {
      count.textContent = state.keywordsCount ? ' (' + state.keywordsCount + ')' : '';
      clear.style.display = state.keywordsCount ? 'inline-block' : 'none';
    }

    toggle.addEventListener('click', function () {
      var open = cloud.style.display === 'none';
      cloud.style.display = open ? 'flex' : 'none';
      toggle.classList.toggle('active', open);
    });

    clear.addEventListener('click', function () {
      state.keywords = Object.create(null);
      state.keywordsCount = 0;
      chips.forEach(function (c) { c.classList.remove('active'); });
      renderCount();
      onChange();
    });

    return wrap;
  }
})();
