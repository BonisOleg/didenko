(function () {
  'use strict';

  var PHONE_PREFIX = '+380';
  var PHONE_DIGITS_AFTER = 9;
  var NAME_FORBIDDEN = /[^\p{L}\s]/u;
  var NAME_STRIP = /[^\p{L}\s]/gu;
  var EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/i;

  var MSG = {
    nameRequired: 'Вкажіть імʼя',
    nameInvalid: 'Лише літери та пробіли',
    phoneRequired: 'Вкажіть номер телефону',
    phoneInvalid: 'Введіть коректний український номер',
    emailRequired: 'Вкажіть email',
    emailInvalid: 'Введіть коректний email',
    consentRequired: 'Потрібна згода з політикою конфіденційності',
  };

  function field(form, name) {
    return form.querySelector('[name="' + name + '"], [name$="-' + name + '"]');
  }

  function errorBox(form, name) {
    return form.querySelector('[data-error-for="' + name + '"]');
  }

  function setError(form, name, message) {
    var input = field(form, name);
    var box = errorBox(form, name);
    if (input) {
      input.classList.toggle('is-invalid', Boolean(message));
      input.setAttribute('aria-invalid', message ? 'true' : 'false');
    }
    if (!box) {
      return;
    }
    if (message) {
      box.textContent = message;
      box.hidden = false;
      box.classList.add('is-visible');
    } else {
      box.textContent = '';
      box.hidden = true;
      box.classList.remove('is-visible');
    }
  }

  function clearError(form, name) {
    setError(form, name, '');
  }

  function phoneDigits(value) {
    return String(value || '').replace(/\D/g, '');
  }

  function formatUaPhone(raw) {
    var digits = phoneDigits(raw);
    if (digits.indexOf('380') === 0) {
      digits = digits.slice(3);
    } else if (digits.charAt(0) === '0') {
      digits = digits.slice(1);
    }
    digits = digits.slice(0, PHONE_DIGITS_AFTER);

    var out = PHONE_PREFIX;
    if (digits.length) {
      out += ' ' + digits.slice(0, 2);
    }
    if (digits.length > 2) {
      out += ' ' + digits.slice(2, 5);
    }
    if (digits.length > 5) {
      out += ' ' + digits.slice(5, 7);
    }
    if (digits.length > 7) {
      out += ' ' + digits.slice(7, 9);
    }
    return out;
  }

  function isValidPhone(value) {
    return /^380\d{9}$/.test(phoneDigits(value));
  }

  function isValidName(value) {
    var trimmed = String(value || '').trim();
    if (!trimmed) {
      return false;
    }
    return !NAME_FORBIDDEN.test(trimmed) && /\p{L}/u.test(trimmed);
  }

  function isValidEmail(value) {
    var trimmed = String(value || '').trim();
    return EMAIL_RE.test(trimmed);
  }

  function sanitizeName(value) {
    return String(value || '').replace(NAME_STRIP, '');
  }

  function caretOffsetFromEnd(input) {
    return input.value.length - (input.selectionEnd || 0);
  }

  function restoreCaretFromEnd(input, fromEnd) {
    var pos = Math.max(0, input.value.length - fromEnd);
    try {
      input.setSelectionRange(pos, pos);
    } catch (err) {
      /* iOS may reject setSelectionRange on some input types */
    }
  }

  function protectPhonePrefix(input, event) {
    var start = input.selectionStart || 0;
    var end = input.selectionEnd || 0;
    var prefixLen = PHONE_PREFIX.length;

    if (event.key === 'Backspace') {
      if (start !== end && start < prefixLen) {
        event.preventDefault();
        input.setSelectionRange(prefixLen, end < prefixLen ? prefixLen : end);
        return;
      }
      if (start === end && start > 0 && start <= prefixLen) {
        event.preventDefault();
        input.setSelectionRange(prefixLen, prefixLen);
      }
      return;
    }

    if (event.key === 'Delete') {
      if (start < prefixLen) {
        event.preventDefault();
        input.setSelectionRange(prefixLen, Math.max(end, prefixLen));
      }
    }
  }

  function onNameInput(form, input) {
    var before = input.value;
    var cleaned = sanitizeName(before);
    if (cleaned !== before) {
      var fromEnd = caretOffsetFromEnd(input);
      input.value = cleaned;
      restoreCaretFromEnd(input, fromEnd);
      setError(form, 'name', MSG.nameInvalid);
      return;
    }
    if (!cleaned.trim()) {
      setError(form, 'name', MSG.nameRequired);
      return;
    }
    clearError(form, 'name');
  }

  function onNameBeforeInput(form, input, event) {
    if (!event.data) {
      return;
    }
    if (NAME_FORBIDDEN.test(event.data)) {
      event.preventDefault();
      setError(form, 'name', MSG.nameInvalid);
    }
  }

  function onPhoneInput(form, input) {
    var fromEnd = caretOffsetFromEnd(input);
    var next = formatUaPhone(input.value);
    if (input.value !== next) {
      input.value = next;
      restoreCaretFromEnd(input, fromEnd);
    }
    if (phoneDigits(input.value).length <= 3) {
      setError(form, 'phone', MSG.phoneRequired);
      return;
    }
    if (!isValidPhone(input.value)) {
      setError(form, 'phone', MSG.phoneInvalid);
      return;
    }
    clearError(form, 'phone');
  }

  function onEmailInput(form, input) {
    var value = input.value.trim();
    if (!value) {
      setError(form, 'email', MSG.emailRequired);
      return;
    }
    if (!isValidEmail(value)) {
      setError(form, 'email', MSG.emailInvalid);
      return;
    }
    clearError(form, 'email');
  }

  function validateName(form, input, showEmpty) {
    var value = input ? input.value : '';
    if (!String(value).trim()) {
      if (showEmpty) {
        setError(form, 'name', MSG.nameRequired);
      }
      return false;
    }
    if (!isValidName(value)) {
      setError(form, 'name', MSG.nameInvalid);
      return false;
    }
    clearError(form, 'name');
    return true;
  }

  function validatePhone(form, input, showEmpty) {
    var value = input ? input.value : '';
    if (phoneDigits(value).length <= 3) {
      if (showEmpty) {
        setError(form, 'phone', MSG.phoneRequired);
      }
      return false;
    }
    if (!isValidPhone(value)) {
      setError(form, 'phone', MSG.phoneInvalid);
      return false;
    }
    clearError(form, 'phone');
    return true;
  }

  function validateEmail(form, input, showEmpty) {
    var value = input ? String(input.value || '').trim() : '';
    if (!value) {
      if (showEmpty) {
        setError(form, 'email', MSG.emailRequired);
      }
      return false;
    }
    if (!isValidEmail(value)) {
      setError(form, 'email', MSG.emailInvalid);
      return false;
    }
    clearError(form, 'email');
    return true;
  }

  function validateConsent(form, input, showEmpty) {
    if (input && input.checked) {
      clearError(form, 'consent');
      return true;
    }
    if (showEmpty) {
      setError(form, 'consent', MSG.consentRequired);
    }
    return false;
  }

  function validateForm(form) {
    var nameOk = validateName(form, field(form, 'name'), true);
    var phoneOk = validatePhone(form, field(form, 'phone'), true);
    var emailOk = validateEmail(form, field(form, 'email'), true);
    var consentOk = validateConsent(form, field(form, 'consent'), true);
    return nameOk && phoneOk && emailOk && consentOk;
  }

  function focusFirstInvalid(form) {
    var invalid = form.querySelector('.is-invalid');
    if (invalid && typeof invalid.focus === 'function') {
      invalid.focus();
    }
  }

  function bindPhoneInitial(input) {
    if (!input) {
      return;
    }
    if (!input.value || phoneDigits(input.value).indexOf('380') !== 0) {
      input.value = formatUaPhone(input.value || PHONE_PREFIX);
    } else {
      input.value = formatUaPhone(input.value);
    }
  }

  function initForm(form) {
    if (!form || form.getAttribute('data-lead-validation') === '1') {
      return;
    }
    form.setAttribute('data-lead-validation', '1');
    bindPhoneInitial(field(form, 'phone'));
    form.querySelectorAll('[data-error-for]').forEach(function (box) {
      if (!box.classList.contains('is-visible')) {
        return;
      }
      if (!String(box.textContent || '').trim()) {
        return;
      }
      var input = field(form, box.getAttribute('data-error-for'));
      if (input) {
        input.classList.add('is-invalid');
        input.setAttribute('aria-invalid', 'true');
      }
    });
  }

  document.querySelectorAll('form.lead-form').forEach(initForm);

  document.body.addEventListener('htmx:afterSwap', function (event) {
    var target = event.detail && event.detail.target;
    if (!target) {
      return;
    }
    if (target.matches && target.matches('form.lead-form')) {
      initForm(target);
      return;
    }
    if (target.querySelectorAll) {
      target.querySelectorAll('form.lead-form').forEach(initForm);
    }
  });

  document.body.addEventListener('beforeinput', function (event) {
    var input = event.target;
    if (!input || !input.closest) {
      return;
    }
    var form = input.closest('form.lead-form');
    if (!form) {
      return;
    }
    if (input === field(form, 'name')) {
      onNameBeforeInput(form, input, event);
    }
  });

  document.body.addEventListener('input', function (event) {
    var input = event.target;
    if (!input || !input.closest) {
      return;
    }
    var form = input.closest('form.lead-form');
    if (!form) {
      return;
    }
    if (input === field(form, 'name')) {
      onNameInput(form, input);
      return;
    }
    if (input === field(form, 'phone')) {
      onPhoneInput(form, input);
      return;
    }
    if (input === field(form, 'email')) {
      onEmailInput(form, input);
      return;
    }
    if (input === field(form, 'consent')) {
      validateConsent(form, input, true);
    }
  });

  document.body.addEventListener('keydown', function (event) {
    var input = event.target;
    if (!input || !input.closest) {
      return;
    }
    var form = input.closest('form.lead-form');
    if (!form || input !== field(form, 'phone')) {
      return;
    }
    protectPhonePrefix(input, event);
  });

  document.body.addEventListener('blur', function (event) {
    var input = event.target;
    if (!input || !input.closest) {
      return;
    }
    var form = input.closest('form.lead-form');
    if (!form) {
      return;
    }
    if (input === field(form, 'name')) {
      validateName(form, input, true);
      return;
    }
    if (input === field(form, 'phone')) {
      input.value = formatUaPhone(input.value);
      validatePhone(form, input, true);
      return;
    }
    if (input === field(form, 'email')) {
      validateEmail(form, input, true);
    }
  }, true);

  document.body.addEventListener('paste', function (event) {
    var input = event.target;
    if (!input || !input.closest) {
      return;
    }
    var form = input.closest('form.lead-form');
    if (!form) {
      return;
    }
    if (input === field(form, 'phone')) {
      event.preventDefault();
      var text = '';
      try {
        text = (event.clipboardData || window.clipboardData).getData('text') || '';
      } catch (err) {
        text = '';
      }
      input.value = formatUaPhone(PHONE_PREFIX + text);
      onPhoneInput(form, input);
      return;
    }
    if (input === field(form, 'name')) {
      event.preventDefault();
      var pasted = '';
      try {
        pasted = (event.clipboardData || window.clipboardData).getData('text') || '';
      } catch (err2) {
        pasted = '';
      }
      var start = input.selectionStart || 0;
      var end = input.selectionEnd || 0;
      var next = input.value.slice(0, start) + pasted + input.value.slice(end);
      var cleaned = sanitizeName(next);
      input.value = cleaned;
      if (cleaned !== next) {
        setError(form, 'name', MSG.nameInvalid);
      } else if (!cleaned.trim()) {
        setError(form, 'name', MSG.nameRequired);
      } else {
        clearError(form, 'name');
      }
    }
  });

  document.body.addEventListener(
    'submit',
    function (event) {
      var form = event.target;
      if (!form || !form.classList || !form.classList.contains('lead-form')) {
        return;
      }
      initForm(form);
      var phone = field(form, 'phone');
      if (phone) {
        phone.value = formatUaPhone(phone.value);
      }
      if (!validateForm(form)) {
        event.preventDefault();
        event.stopPropagation();
        if (typeof event.stopImmediatePropagation === 'function') {
          event.stopImmediatePropagation();
        }
        focusFirstInvalid(form);
      }
    },
    true
  );
})();
