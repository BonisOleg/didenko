(function () {
  var header = document.getElementById('site-header');
  var toggle = document.querySelector('[data-nav-toggle]');
  var nav = document.querySelector('[data-nav]');
  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var modal = document.getElementById('service-modal');
  var modalContent = document.getElementById('service-modal-content');
  var lastFocus = null;

  if (header) {
    var onScroll = function () {
      header.classList.toggle('is-scrolled', window.scrollY > 8);
    };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      toggle.setAttribute('aria-label', open ? 'Закрити меню' : 'Відкрити меню');
    });

    nav.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', function () {
        if (window.matchMedia('(max-width: 991.98px)').matches) {
          nav.classList.remove('is-open');
          toggle.setAttribute('aria-expanded', 'false');
          toggle.setAttribute('aria-label', 'Відкрити меню');
        }
      });
    });
  }

  var revealObserver = null;

  var bindReveal = function (root) {
    var scope = root || document;
    var nodes = scope.querySelectorAll('[data-reveal]');
    nodes.forEach(function (node) {
      var delay = node.getAttribute('data-reveal-delay');
      if (delay !== null && delay !== '') {
        var ms = String(Number(delay) * 150) + 'ms';
        node.style.setProperty('--audience-delay', ms);
        node.style.setProperty('--service-delay', ms);
        node.style.setProperty('--advantage-delay', ms);
        node.style.setProperty('--blog-delay', ms);
        node.style.setProperty('--about-delay', ms);
      }
    });

    if (!nodes.length) {
      return;
    }

    if (reduceMotion || !('IntersectionObserver' in window)) {
      nodes.forEach(function (node) {
        node.classList.add('is-visible');
      });
      return;
    }

    if (!revealObserver) {
      revealObserver = new IntersectionObserver(
        function (entries) {
          entries.forEach(function (entry) {
            if (entry.isIntersecting) {
              entry.target.classList.add('is-visible');
              revealObserver.unobserve(entry.target);
            }
          });
        },
        { threshold: 0.14, rootMargin: '0px 0px -8% 0px' }
      );
    }

    nodes.forEach(function (node) {
      if (!node.classList.contains('is-visible')) {
        revealObserver.observe(node);
      }
    });
  };

  bindReveal(document);

  var animateCount = function (node) {
    var target = Number(node.getAttribute('data-count'));
    if (!isFinite(target)) {
      return;
    }
    var suffix = node.getAttribute('data-suffix') || '';
    var prefix = node.getAttribute('data-prefix') || '';
    var duration = 1200;
    var start = null;

    var step = function (ts) {
      if (start === null) {
        start = ts;
      }
      var progress = Math.min((ts - start) / duration, 1);
      var eased = 1 - Math.pow(1 - progress, 3);
      var value = Math.round(target * eased);
      node.textContent = prefix + String(value) + suffix;
      if (progress < 1) {
        window.requestAnimationFrame(step);
      }
    };

    if (reduceMotion) {
      node.textContent = prefix + String(target) + suffix;
      return;
    }
    window.requestAnimationFrame(step);
  };

  var bindCounters = function (root) {
    var scope = root || document;
    var nodes = scope.querySelectorAll('[data-count]');
    if (!nodes.length) {
      return;
    }
    if (reduceMotion || !('IntersectionObserver' in window)) {
      nodes.forEach(animateCount);
      return;
    }
    var counterObserver = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) {
            return;
          }
          animateCount(entry.target);
          counterObserver.unobserve(entry.target);
        });
      },
      { threshold: 0.35 }
    );
    nodes.forEach(function (node) {
      counterObserver.observe(node);
    });
  };

  bindCounters(document);

  var checklist = document.querySelector('[data-audience-checklist]');
  var cta = document.querySelector('[data-audience-cta]');
  var countNode = document.querySelector('[data-audience-count]');

  var getSelectedAudienceTopics = function () {
    if (!checklist) {
      return [];
    }
    var topics = [];
    checklist.querySelectorAll('[data-audience-item].is-selected').forEach(function (item) {
      var text = (item.getAttribute('data-audience-text') || '').trim();
      if (!text) {
        var textNode = item.querySelector('.audience-card__text');
        text = textNode ? textNode.textContent.trim() : '';
      }
      if (text && topics.indexOf(text) === -1) {
        topics.push(text);
      }
    });
    return topics;
  };

  var syncSelectedTopicsToForms = function () {
    var json = JSON.stringify(getSelectedAudienceTopics());
    document.querySelectorAll('[data-selected-topics]').forEach(function (input) {
      input.value = json;
    });
  };

  if (checklist && cta) {
    var items = checklist.querySelectorAll('[data-audience-item]');

    var syncAudienceCta = function () {
      var selected = checklist.querySelectorAll('[data-audience-item].is-selected').length;
      cta.classList.toggle('is-visible', selected > 0);
      if (countNode) {
        countNode.textContent = selected > 0 ? String(selected) : '1+';
      }
      syncSelectedTopicsToForms();
    };

    items.forEach(function (item) {
      item.addEventListener('click', function () {
        var selected = item.classList.toggle('is-selected');
        item.setAttribute('aria-pressed', selected ? 'true' : 'false');
        syncAudienceCta();
      });
    });

    syncAudienceCta();
  } else {
    syncSelectedTopicsToForms();
  }

  document.body.addEventListener('htmx:afterSwap', function () {
    syncSelectedTopicsToForms();
  });

  document.body.addEventListener(
    'submit',
    function (event) {
      var form = event.target;
      if (!form || !form.classList || !form.classList.contains('lead-form')) {
        return;
      }
      syncSelectedTopicsToForms();
    },
    true
  );

  var blogFilters = document.querySelectorAll('[data-blog-filter]');
  blogFilters.forEach(function (btn) {
    btn.addEventListener('click', function () {
      blogFilters.forEach(function (other) {
        other.classList.remove('is-active');
        other.setAttribute('aria-selected', 'false');
      });
      btn.classList.add('is-active');
      btn.setAttribute('aria-selected', 'true');
    });
  });

  var syncBlogPills = function (activeEl) {
    var pills = document.querySelectorAll('[data-blog-pill]');
    pills.forEach(function (pill) {
      var on = pill === activeEl;
      pill.classList.toggle('is-active', on);
      pill.setAttribute('aria-selected', on ? 'true' : 'false');
    });
  };

  document.body.addEventListener('click', function (event) {
    var pill = event.target.closest('[data-blog-pill]');
    if (!pill) {
      return;
    }
    syncBlogPills(pill);
  });

  var openModal = function () {
    if (!modal) {
      return;
    }
    lastFocus = document.activeElement;
    modal.hidden = false;
    modal.classList.add('is-open');
    modal.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
    var closeBtn = modal.querySelector('[data-modal-close].service-modal__close');
    if (closeBtn) {
      closeBtn.focus();
    }
  };

  var closeModal = function () {
    if (!modal) {
      return;
    }
    modal.classList.remove('is-open');
    modal.hidden = true;
    modal.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
    if (modalContent) {
      modalContent.innerHTML = '<p class="service-modal__loading">Завантаження…</p>';
    }
    if (lastFocus && typeof lastFocus.focus === 'function') {
      lastFocus.focus();
    }
  };

  if (modal) {
    modal.addEventListener('click', function (event) {
      var closer = event.target.closest('[data-modal-close]');
      if (!closer) {
        return;
      }
      closeModal();
    });

    document.addEventListener('keydown', function (event) {
      if (event.key === 'Escape' && modal.classList.contains('is-open')) {
        closeModal();
      }
    });
  }

  document.body.addEventListener('htmx:beforeRequest', function (event) {
    var elt = event.detail && event.detail.elt;
    if (!elt || !elt.classList.contains('service-card__more') || !modalContent) {
      return;
    }
    modalContent.innerHTML = '<p class="service-modal__loading">Завантаження…</p>';
    openModal();
  });

  document.body.addEventListener('htmx:afterSwap', function (event) {
    var target = event.detail && event.detail.target;
    if (!target) {
      return;
    }
    if (target.id === 'service-modal-content') {
      openModal();
    }
    if (target.id === 'home-blog-grid') {
      bindReveal(target);
    }
    if (target.id === 'blog-posts-container') {
      bindReveal(target);
    }
  });

  var leadModal = document.getElementById('lead-modal');
  var leadLastFocus = null;

  var openLeadModal = function () {
    if (!leadModal) {
      return;
    }
    leadLastFocus = document.activeElement;
    leadModal.hidden = false;
    leadModal.classList.add('is-open');
    leadModal.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
    var closeBtn = leadModal.querySelector('[data-lead-close].lead-modal__close');
    if (closeBtn) {
      closeBtn.focus();
    }
  };

  var closeLeadModal = function () {
    if (!leadModal) {
      return;
    }
    leadModal.classList.remove('is-open');
    leadModal.hidden = true;
    leadModal.setAttribute('aria-hidden', 'true');
    if (!modal || !modal.classList.contains('is-open')) {
      document.body.style.overflow = '';
    }
    if (leadLastFocus && typeof leadLastFocus.focus === 'function') {
      leadLastFocus.focus();
    }
  };

  document.body.addEventListener('click', function (event) {
    var opener = event.target.closest('[data-lead-open]');
    if (opener) {
      var rippleBtn = opener.classList.contains('btn-cta-primary')
        ? opener
        : opener.closest('.btn-cta-primary');
      if (rippleBtn) {
        var rect = rippleBtn.getBoundingClientRect();
        var rx = ((event.clientX - rect.left) / rect.width) * 100;
        var ry = ((event.clientY - rect.top) / rect.height) * 100;
        rippleBtn.style.setProperty('--rx', rx + '%');
        rippleBtn.style.setProperty('--ry', ry + '%');
        rippleBtn.classList.remove('is-rippling');
        void rippleBtn.offsetWidth;
        rippleBtn.classList.add('is-rippling');
        window.setTimeout(function () {
          rippleBtn.classList.remove('is-rippling');
        }, 450);
      }
      openLeadModal();
      return;
    }
    if (!leadModal) {
      return;
    }
    var closer = event.target.closest('[data-lead-close]');
    if (closer && leadModal.contains(closer)) {
      closeLeadModal();
    }
  });

  document.addEventListener('keydown', function (event) {
    if (event.key !== 'Escape') {
      return;
    }
    if (leadModal && leadModal.classList.contains('is-open')) {
      closeLeadModal();
    }
  });

  var copyToastTimer = null;
  var ensureCopyToast = function () {
    var toast = document.getElementById('copy-toast');
    if (toast) {
      return toast;
    }
    toast = document.createElement('div');
    toast.id = 'copy-toast';
    toast.className = 'copy-toast';
    toast.setAttribute('role', 'status');
    toast.setAttribute('aria-live', 'polite');
    document.body.appendChild(toast);
    return toast;
  };

  var showCopyToast = function (message) {
    var toast = ensureCopyToast();
    toast.textContent = message || 'Скопійовано';
    toast.classList.add('is-visible');
    if (copyToastTimer) {
      window.clearTimeout(copyToastTimer);
    }
    copyToastTimer = window.setTimeout(function () {
      toast.classList.remove('is-visible');
    }, 2200);
  };

  var copyText = function (text) {
    if (navigator.clipboard && typeof navigator.clipboard.writeText === 'function') {
      return navigator.clipboard.writeText(text);
    }
    return new Promise(function (resolve, reject) {
      var area = document.createElement('textarea');
      area.value = text;
      area.setAttribute('readonly', '');
      area.style.position = 'fixed';
      area.style.opacity = '0';
      document.body.appendChild(area);
      area.select();
      try {
        var ok = document.execCommand('copy');
        document.body.removeChild(area);
        if (ok) {
          resolve();
        } else {
          reject(new Error('copy failed'));
        }
      } catch (err) {
        document.body.removeChild(area);
        reject(err);
      }
    });
  };

  document.body.addEventListener('click', function (event) {
    var copyBtn = event.target.closest('[data-copy]');
    if (!copyBtn) {
      return;
    }
    var value = copyBtn.getAttribute('data-copy');
    if (!value) {
      return;
    }
    event.preventDefault();
    copyText(value).then(function () {
      showCopyToast(copyBtn.getAttribute('data-copy-toast') || 'Скопійовано');
    }).catch(function () {
      showCopyToast('Не вдалося скопіювати');
    });
  });
})();
