(function () {
  'use strict';

  function renumber(root) {
    var rows = root.querySelectorAll('[data-json-list-row]');
    rows.forEach(function (row, index) {
      var label = row.querySelector('.json-list-widget__row-index');
      if (!label) return;
      var base = label.textContent.replace(/\s*\d+\s*$/, '').trim() || 'Пункт';
      label.textContent = base + ' ' + (index + 1);
    });
  }

  function bindRoot(root) {
    if (root.dataset.jsonListBound === '1') return;
    root.dataset.jsonListBound = '1';

    var items = root.querySelector('[data-json-list-items]');
    var template = root.querySelector('[data-json-list-template]');
    var addBtn = root.querySelector('[data-json-list-add]');
    if (!items || !template || !addBtn) return;

    addBtn.addEventListener('click', function () {
      var node = template.content.cloneNode(true);
      items.appendChild(node);
      renumber(root);
      var focusEl = items.lastElementChild && items.lastElementChild.querySelector('textarea, input');
      if (focusEl) focusEl.focus();
    });

    root.addEventListener('click', function (event) {
      var btn = event.target.closest('[data-json-list-remove]');
      if (!btn || !root.contains(btn)) return;
      var row = btn.closest('[data-json-list-row]');
      if (!row) return;
      var rows = items.querySelectorAll('[data-json-list-row]');
      if (rows.length <= 1) {
        row.querySelectorAll('textarea, input').forEach(function (el) {
          el.value = '';
        });
        renumber(root);
        return;
      }
      row.remove();
      renumber(root);
    });
  }

  function init(scope) {
    (scope || document).querySelectorAll('[data-json-list]').forEach(bindRoot);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () {
      init(document);
    });
  } else {
    init(document);
  }

  document.addEventListener('formset:added', function (event) {
    init(event.target);
  });
})();
