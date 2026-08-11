(function () {
  'use strict';

  var FIELD_MAP = {
    audience: ['payload_intro', 'payload_items_strings'],
    advantages: ['payload_intro', 'payload_items_cards'],
    services_teaser: ['payload_limit'],
    blog_teaser: ['payload_limit'],
    lead_form: ['payload_heading', 'payload_anchor'],
  };

  var ALL_FIELDS = [
    'payload_intro',
    'payload_items_strings',
    'payload_items_cards',
    'payload_limit',
    'payload_heading',
    'payload_anchor',
  ];

  function findFieldRow(name) {
    var byClass = document.querySelector('.field-' + name);
    if (byClass) return byClass;

    var byId = document.getElementById('id_' + name);
    if (byId) {
      return (
        byId.closest('.form-row') ||
        byId.closest('[class*="field-"]') ||
        byId.closest('.flex') ||
        byId.parentElement
      );
    }

    var named = document.querySelector(
      '[name="' + name + '"], [name="' + name + '__title"], [name="' + name + '__label"]'
    );
    if (!named) return null;
    return (
      named.closest('.form-row') ||
      named.closest('[class*="field-"]') ||
      named.closest('.json-list-widget') && named.closest('[class*="field-"]') ||
      named.closest('.flex') ||
      named.parentElement
    );
  }

  function setVisible(el, visible) {
    if (!el) return;
    el.hidden = !visible;
    el.style.display = visible ? '' : 'none';
    el.querySelectorAll('input, textarea, select').forEach(function (control) {
      if (visible) {
        control.removeAttribute('disabled');
      } else {
        control.setAttribute('disabled', 'disabled');
      }
    });
  }

  function applyType(type) {
    var active = FIELD_MAP[type] || [];
    ALL_FIELDS.forEach(function (name) {
      setVisible(findFieldRow(name), active.indexOf(name) !== -1);
    });
  }

  function init() {
    var typeSelect = document.getElementById('id_block_type');
    if (!typeSelect) return;
    applyType(typeSelect.value);
    typeSelect.addEventListener('change', function () {
      applyType(typeSelect.value);
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
