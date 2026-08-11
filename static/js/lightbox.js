(function () {
  var ROOT_SELECTORS = [
    '.about-page',
    '.case-detail',
    '.blog-page',
    '.blog-teaser-grid',
  ];
  var SKIP_CLOSEST =
    '.site-header, .site-footer, .lightbox, [data-no-lightbox], button, .btn';

  var items = [];
  var index = 0;
  var lastFocus = null;
  var scale = 1;
  var tx = 0;
  var ty = 0;
  var minScale = 1;
  var maxScale = 4;
  var pointers = new Map();
  var pinchStartDist = 0;
  var pinchStartScale = 1;
  var panStartX = 0;
  var panStartY = 0;
  var panOriginX = 0;
  var panOriginY = 0;
  var swipeStartX = 0;
  var swipeStartY = 0;
  var swipeActive = false;
  var lastTapAt = 0;

  var root = null;
  var stage = null;
  var figure = null;
  var imgEl = null;
  var captionEl = null;
  var counterEl = null;
  var prevBtn = null;
  var nextBtn = null;

  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  var ensureDom = function () {
    if (root) {
      return;
    }
    root = document.createElement('div');
    root.className = 'lightbox';
    root.id = 'site-lightbox';
    root.hidden = true;
    root.setAttribute('aria-hidden', 'true');
    root.innerHTML =
      '<div class="lightbox__backdrop" data-lightbox-close tabindex="-1"></div>' +
      '<button type="button" class="lightbox__close" data-lightbox-close aria-label="Закрити">×</button>' +
      '<div class="lightbox__counter" aria-live="polite"></div>' +
      '<button type="button" class="lightbox__nav lightbox__nav--prev" aria-label="Попереднє фото">' +
      '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M15 5 8 12l7 7" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>' +
      '</button>' +
      '<button type="button" class="lightbox__nav lightbox__nav--next" aria-label="Наступне фото">' +
      '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M9 5l7 7-7 7" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>' +
      '</button>' +
      '<div class="lightbox__stage">' +
      '<figure class="lightbox__figure">' +
      '<img class="lightbox__img" alt="">' +
      '</figure>' +
      '</div>' +
      '<p class="lightbox__caption"></p>';
    document.body.appendChild(root);

    stage = root.querySelector('.lightbox__stage');
    figure = root.querySelector('.lightbox__figure');
    imgEl = root.querySelector('.lightbox__img');
    captionEl = root.querySelector('.lightbox__caption');
    counterEl = root.querySelector('.lightbox__counter');
    prevBtn = root.querySelector('.lightbox__nav--prev');
    nextBtn = root.querySelector('.lightbox__nav--next');

    root.addEventListener('click', function (event) {
      if (event.target.closest('[data-lightbox-close]')) {
        close();
      }
    });
    prevBtn.addEventListener('click', function (event) {
      event.stopPropagation();
      show(index - 1);
    });
    nextBtn.addEventListener('click', function (event) {
      event.stopPropagation();
      show(index + 1);
    });

    stage.addEventListener('pointerdown', onPointerDown);
    stage.addEventListener('pointermove', onPointerMove);
    stage.addEventListener('pointerup', onPointerUp);
    stage.addEventListener('pointercancel', onPointerUp);
    stage.addEventListener('wheel', onWheel, { passive: false });
  };

  var isZoomable = function (img) {
    if (!img || img.tagName !== 'IMG') {
      return false;
    }
    if (!img.getAttribute('src') && !img.currentSrc) {
      return false;
    }
    if (img.closest(SKIP_CLOSEST)) {
      return false;
    }
    if (img.classList.contains('lightbox__img')) {
      return false;
    }
    var w = img.naturalWidth || img.width || 0;
    var h = img.naturalHeight || img.height || 0;
    if (w && h && w < 48 && h < 48) {
      return false;
    }
    return true;
  };

  var fullSrc = function (img) {
    var link = img.closest('a[href]');
    if (link) {
      var href = link.getAttribute('href') || '';
      if (/\.(jpe?g|png|gif|webp|avif|svg)(\?|#|$)/i.test(href)) {
        return href;
      }
    }
    return img.currentSrc || img.src;
  };

  var toItem = function (img) {
    return {
      src: fullSrc(img),
      alt: img.getAttribute('alt') || '',
      el: img,
    };
  };

  var resolveGroupScope = function (img) {
    if (!img) {
      return null;
    }
    var named = img.closest('[data-lightbox-group], .about-gallery');
    if (named) {
      return named;
    }
    var article = img.closest('.case-detail');
    if (article) {
      return article;
    }
    if (img.closest('.blog-card, .post-card, .post-card__featured-visual')) {
      return img;
    }
    if (img.closest('.about-hero__frame, .about-hero__card')) {
      return img;
    }
    return img.closest('.about-block') || img;
  };

  var collectFromRoot = function (scopeRoot, trigger) {
    if (!scopeRoot) {
      return { list: [], start: 0 };
    }
    if (scopeRoot.tagName === 'IMG') {
      return { list: [toItem(scopeRoot)], start: 0 };
    }
    var list = [];
    var start = 0;
    scopeRoot.querySelectorAll('img').forEach(function (img) {
      if (!isZoomable(img)) {
        return;
      }
      var ownGroup = resolveGroupScope(img);
      if (ownGroup !== scopeRoot && ownGroup !== img) {
        return;
      }
      if (img === trigger) {
        start = list.length;
      }
      list.push(toItem(img));
    });
    if (!list.length && trigger) {
      return { list: [toItem(trigger)], start: 0 };
    }
    return { list: list, start: start };
  };

  var applyTransform = function () {
    if (!figure) {
      return;
    }
    figure.style.transform =
      'translate3d(' + tx + 'px,' + ty + 'px,0) scale(' + scale + ')';
  };

  var resetZoom = function () {
    scale = 1;
    tx = 0;
    ty = 0;
    applyTransform();
  };

  var clampPan = function () {
    if (!stage || !imgEl || scale <= 1.01) {
      tx = 0;
      ty = 0;
      return;
    }
    var rect = imgEl.getBoundingClientRect();
    var maxX = Math.max(0, (rect.width - stage.clientWidth) / 2 + 24);
    var maxY = Math.max(0, (rect.height - stage.clientHeight) / 2 + 24);
    tx = Math.min(maxX, Math.max(-maxX, tx));
    ty = Math.min(maxY, Math.max(-maxY, ty));
  };

  var updateChrome = function () {
    var total = items.length;
    var multi = total > 1;
    prevBtn.hidden = !multi;
    nextBtn.hidden = !multi;
    counterEl.textContent = multi ? index + 1 + ' / ' + total : '';
    counterEl.hidden = !multi;
  };

  var show = function (nextIndex) {
    if (!items.length) {
      return;
    }
    index = ((nextIndex % items.length) + items.length) % items.length;
    var item = items[index];
    resetZoom();
    imgEl.onload = function () {
      resetZoom();
    };
    imgEl.onerror = function () {
      captionEl.textContent = 'Не вдалося завантажити зображення';
    };
    imgEl.src = item.src;
    imgEl.alt = item.alt || '';
    captionEl.textContent = item.alt || '';
    updateChrome();
  };

  var open = function (list, startIndex) {
    if (!list || !list.length) {
      return;
    }
    ensureDom();
    items = list;
    lastFocus = document.activeElement;
    root.hidden = false;
    root.classList.add('is-open');
    root.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
    show(startIndex || 0);
    root.querySelector('.lightbox__close').focus();
  };

  var close = function () {
    if (!root || root.hidden) {
      return;
    }
    root.classList.remove('is-open');
    root.hidden = true;
    root.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
    items = [];
    resetZoom();
    imgEl.removeAttribute('src');
    if (lastFocus && typeof lastFocus.focus === 'function') {
      lastFocus.focus();
    }
  };

  var distance = function (a, b) {
    var dx = a.clientX - b.clientX;
    var dy = a.clientY - b.clientY;
    return Math.sqrt(dx * dx + dy * dy);
  };

  var onPointerDown = function (event) {
    if (!root || root.hidden) {
      return;
    }
    stage.setPointerCapture(event.pointerId);
    pointers.set(event.pointerId, event);

    if (pointers.size === 2) {
      var pts = Array.from(pointers.values());
      pinchStartDist = distance(pts[0], pts[1]);
      pinchStartScale = scale;
      swipeActive = false;
      return;
    }

    if (scale > 1.01) {
      panStartX = event.clientX;
      panStartY = event.clientY;
      panOriginX = tx;
      panOriginY = ty;
      swipeActive = false;
    } else {
      swipeStartX = event.clientX;
      swipeStartY = event.clientY;
      swipeActive = true;
    }

    var now = Date.now();
    if (now - lastTapAt < 280 && event.pointerType !== 'mouse') {
      if (scale > 1.05) {
        resetZoom();
      } else {
        scale = 2.2;
        applyTransform();
      }
      lastTapAt = 0;
    } else {
      lastTapAt = now;
    }
  };

  var onPointerMove = function (event) {
    if (!pointers.has(event.pointerId)) {
      return;
    }
    pointers.set(event.pointerId, event);

    if (pointers.size === 2) {
      event.preventDefault();
      var pts = Array.from(pointers.values());
      var dist = distance(pts[0], pts[1]);
      if (pinchStartDist > 0) {
        scale = Math.min(
          maxScale,
          Math.max(minScale, pinchStartScale * (dist / pinchStartDist))
        );
        if (scale <= 1.01) {
          scale = 1;
          tx = 0;
          ty = 0;
        }
        clampPan();
        applyTransform();
      }
      return;
    }

    if (scale > 1.01) {
      event.preventDefault();
      tx = panOriginX + (event.clientX - panStartX);
      ty = panOriginY + (event.clientY - panStartY);
      clampPan();
      applyTransform();
    }
  };

  var onPointerUp = function (event) {
    if (!pointers.has(event.pointerId)) {
      return;
    }
    var startEvent = pointers.get(event.pointerId);
    pointers.delete(event.pointerId);

    if (pointers.size < 2) {
      pinchStartDist = 0;
    }

    if (swipeActive && scale <= 1.01 && items.length > 1 && startEvent) {
      var dx = event.clientX - swipeStartX;
      var dy = event.clientY - swipeStartY;
      if (Math.abs(dx) > 56 && Math.abs(dx) > Math.abs(dy) * 1.2) {
        show(index + (dx < 0 ? 1 : -1));
      }
    }
    swipeActive = false;
  };

  var onWheel = function (event) {
    if (!root || root.hidden) {
      return;
    }
    event.preventDefault();
    var next = scale + (event.deltaY < 0 ? 0.18 : -0.18);
    scale = Math.min(maxScale, Math.max(minScale, next));
    if (scale <= 1.01) {
      resetZoom();
      return;
    }
    clampPan();
    applyTransform();
  };

  var enhanceImage = function (img) {
    if (!isZoomable(img) || img.dataset.lightboxBound === '1') {
      return;
    }
    img.dataset.lightboxBound = '1';
    img.classList.add('is-lightbox-trigger');
    img.setAttribute('tabindex', '0');
    img.setAttribute('role', 'button');
    if (!img.getAttribute('aria-label')) {
      var alt = (img.getAttribute('alt') || '').trim();
      img.setAttribute(
        'aria-label',
        alt ? 'Збільшити: ' + alt : 'Збільшити зображення'
      );
    }

    var heroFrame = img.closest('.about-hero__frame');
    if (heroFrame) {
      heroFrame.classList.add('is-lightbox-trigger');
    }
  };

  var bindRoot = function (scopeRoot) {
    if (!scopeRoot) {
      return;
    }
    scopeRoot.querySelectorAll('img').forEach(enhanceImage);
    if (scopeRoot.dataset.lightboxRoot === '1') {
      return;
    }
    scopeRoot.dataset.lightboxRoot = '1';

    scopeRoot.addEventListener('click', function (event) {
      var img = event.target.closest('img');
      if (!img || !scopeRoot.contains(img) || !isZoomable(img)) {
        return;
      }
      event.preventDefault();
      event.stopPropagation();
      var packed = collectFromRoot(resolveGroupScope(img), img);
      open(packed.list, packed.start);
    });

    scopeRoot.addEventListener('keydown', function (event) {
      if (event.key !== 'Enter' && event.key !== ' ') {
        return;
      }
      var img = event.target.closest('img');
      if (!img || !scopeRoot.contains(img) || !isZoomable(img)) {
        return;
      }
      event.preventDefault();
      var packed = collectFromRoot(resolveGroupScope(img), img);
      open(packed.list, packed.start);
    });
  };

  var scan = function (rootNode) {
    var scope = rootNode || document;
    ROOT_SELECTORS.forEach(function (selector) {
      scope.querySelectorAll(selector).forEach(bindRoot);
      if (scope.matches && scope.matches(selector)) {
        bindRoot(scope);
      }
    });
  };

  document.addEventListener('keydown', function (event) {
    if (!root || root.hidden) {
      return;
    }
    if (event.key === 'Escape') {
      close();
    } else if (event.key === 'ArrowLeft' && items.length > 1) {
      show(index - 1);
    } else if (event.key === 'ArrowRight' && items.length > 1) {
      show(index + 1);
    }
  });

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () {
      scan(document);
    });
  } else {
    scan(document);
  }

  document.body.addEventListener('htmx:afterSwap', function (event) {
    var target = event.detail && event.detail.target;
    scan(target || document);
  });

  if (reduceMotion) {
    maxScale = 2.5;
  }
})();
