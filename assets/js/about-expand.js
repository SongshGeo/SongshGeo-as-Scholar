/* about-expand.js
 *
 * The About block on the landing page shows only the lede paragraph; the rest
 * of the author bio (content/<lang>/authors/admin/_index.md body) is folded
 * away. This adds the "expand" affordance that fold always implied.
 *
 * Progressive enhancement: the SCSS only hides paragraphs while
 * `.article-style` carries `.is-collapsed`, and that class is added here. With
 * JS off — or if this file fails — the full bio renders, same as in print.
 */
(function () {
  'use strict';

  var IS_ZH = (document.documentElement.lang || '').toLowerCase().indexOf('zh') === 0;

  var L = {
    more: IS_ZH ? '展开全文' : 'Read more',
    less: IS_ZH ? '收起' : 'Show less',
    aria: IS_ZH ? '展开或收起完整简介' : 'Expand or collapse the full bio',
  };

  if (document.readyState !== 'loading') init();
  else document.addEventListener('DOMContentLoaded', init);

  function init() {
    var bodies = document.querySelectorAll('.wg-about .article-style');
    for (var i = 0; i < bodies.length; i++) upgrade(bodies[i], i);
  }

  function upgrade(body, index) {
    if (body.classList.contains('is-collapsed')) return; // idempotent

    // Nothing to fold away: a single paragraph and no trailing link list.
    var hidden = body.querySelectorAll('p:nth-of-type(n + 2), ul');
    if (!hidden.length) return;

    if (!body.id) body.id = 'about-body-' + index;
    body.classList.add('is-collapsed');

    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'about-expand-toggle';
    btn.setAttribute('aria-expanded', 'false');
    btn.setAttribute('aria-controls', body.id);
    btn.setAttribute('aria-label', L.aria);
    btn.innerHTML =
      '<span class="about-expand-text">' + L.more + '</span>' +
      '<span class="about-expand-caret" aria-hidden="true"></span>';

    body.parentNode.insertBefore(btn, body.nextSibling);

    btn.addEventListener('click', function () {
      var collapsed = body.classList.toggle('is-collapsed');
      btn.setAttribute('aria-expanded', collapsed ? 'false' : 'true');
      btn.querySelector('.about-expand-text').textContent = collapsed ? L.more : L.less;
      // Keep the toggle in view when a long bio folds back up.
      // Guarded: not every environment implements scrollIntoView.
      if (collapsed && btn.scrollIntoView) btn.scrollIntoView({ block: 'nearest' });
    });
  }
})();
