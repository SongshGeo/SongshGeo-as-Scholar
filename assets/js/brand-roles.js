/* brand-roles.js
 *
 * Converts the .navbar-brand "SongshGeo" link into an identity-switcher
 * dropdown. Clicking the brand opens a small editorial popover offering
 * three personas: scientist (this site), explorer (blog), developer (GitHub).
 *
 * Both the desktop and mobile brand elements are upgraded.
 */
(function () {
  'use strict';

  // Everything visible here has a single source of truth outside this file:
  // labels in i18n/<lang>.yaml, destinations in data/brand_roles.yaml, and the
  // brand text from the author page (content/<lang>/authors/admin/_index.md).
  // They arrive via window.__siteUI — see layouts/partials/custom_js.html.
  var L = (window.__siteUI || {}).brand;
  if (!L || !L.roles || !L.roles.length) return;
  var ROLES = L.roles;

  if (document.readyState !== 'loading') init();
  else document.addEventListener('DOMContentLoaded', init);

  function init() {
    var brands = document.querySelectorAll('.navbar-brand');
    brands.forEach(upgrade);

    document.addEventListener('click', function (e) {
      if (!e.target.closest('.brand-roles-wrap')) closeAll();
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' || e.keyCode === 27) closeAll();
    });
  }

  function upgrade(brand) {
    if (brand.classList.contains('brand-roles-trigger')) return; // idempotent

    var wrap = brand.parentElement;
    if (!wrap) return;
    wrap.classList.add('brand-roles-wrap');

    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = brand.className + ' brand-roles-trigger';
    btn.setAttribute('aria-haspopup', 'true');
    btn.setAttribute('aria-expanded', 'false');
    btn.setAttribute('aria-label', L.aria);
    btn.innerHTML =
      '<span class="brand-roles-text">' + L.text + '</span>' +
      '<span class="brand-roles-caret" aria-hidden="true"></span>';
    wrap.replaceChild(btn, brand);

    var menu = document.createElement('div');
    menu.className = 'brand-roles-menu';
    menu.setAttribute('role', 'menu');
    menu.hidden = true;

    var eyebrow = document.createElement('div');
    eyebrow.className = 'brand-roles-eyebrow';
    eyebrow.textContent = L.eyebrow;
    menu.appendChild(eyebrow);

    ROLES.forEach(function (r) {
      var a = document.createElement('a');
      a.className = 'brand-role-item' + (r.current ? ' is-current' : '');
      a.href = r.url;
      a.setAttribute('role', 'menuitem');
      if (r.external) { a.target = '_blank'; a.rel = 'noopener'; }
      a.innerHTML =
        '<span class="brand-role-label">' + r.label + '</span>' +
        '<span class="brand-role-sub">' + r.sub + '</span>';
      menu.appendChild(a);
    });

    wrap.appendChild(menu);

    btn.addEventListener('click', function (e) {
      e.preventDefault();
      e.stopPropagation();
      var willOpen = menu.hidden;
      closeAll();
      if (willOpen) {
        menu.hidden = false;
        btn.setAttribute('aria-expanded', 'true');
      }
    });
  }

  function closeAll() {
    var menus = document.querySelectorAll('.brand-roles-menu');
    for (var i = 0; i < menus.length; i++) menus[i].hidden = true;
    var btns = document.querySelectorAll('.brand-roles-trigger');
    for (var j = 0; j < btns.length; j++) btns[j].setAttribute('aria-expanded', 'false');
  }
})();
