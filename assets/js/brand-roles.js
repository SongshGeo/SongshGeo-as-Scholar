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

  var IS_ZH = (document.documentElement.lang || '').toLowerCase().indexOf('zh') === 0;

  var ROLES = IS_ZH ? [
    { label: '作为研究者', sub: '学术主页',          url: '/',                              current: true },
    { label: '作为探索者', sub: '随笔与博客',        url: 'https://songshgeo.com/',         external: true },
    { label: '作为开发者', sub: 'GitHub 开源仓库',   url: 'https://github.com/SongshGeo',   external: true },
  ] : [
    { label: 'As a Scientist', sub: 'Academic site',           url: '/',                            current: true },
    { label: 'As an Explorer', sub: 'Essays & longform blog',  url: 'https://songshgeo.com/',       external: true },
    { label: 'As a Developer', sub: 'Open source on GitHub',   url: 'https://github.com/SongshGeo', external: true },
  ];

  var L = {
    eyebrow: IS_ZH ? '身份' : 'Identity',
    aria:    IS_ZH ? '切换身份' : 'Switch identity',
    // Display label shown in the navbar — deliberately decoupled from
    // site.Title (which now reads "Shuang - Scientist" for the browser tab).
    brand:   IS_ZH ? '宋爽' : 'Shuang Song',
  };

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
      '<span class="brand-roles-text">' + L.brand + '</span>' +
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
