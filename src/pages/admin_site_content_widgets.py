"""Dark-readable CMS widgets (admin_cms_blocks_skill)."""

from django.forms import CheckboxInput, FileInput, Select, Textarea, TextInput
from tinymce.widgets import TinyMCE
from unfold.widgets import INPUT_CLASSES, TEXTAREA_CLASSES, AdminTextInputWidget, AdminTextareaWidget

_SKIP_CLASSES = frozenset(
    {
        'bg-white',
        'text-font-default-light',
        'border-base-200',
        'dark:bg-base-900',
        'dark:border-base-700',
        'dark:text-font-default-dark',
    }
)
_FORCE_CLASSES = ('bg-base-900', 'text-base-100', 'border-base-700', 'placeholder-base-400')


def cms_control_classes(base_classes: list[str]) -> list[str]:
    cleaned = [css for css in base_classes if css not in _SKIP_CLASSES]
    for css in _FORCE_CLASSES:
        if css not in cleaned:
            cleaned.append(css)
    return cleaned


class CmsAdminTextInputWidget(AdminTextInputWidget):
    def __init__(self, attrs=None):
        super().__init__(attrs)
        self.attrs['class'] = ' '.join(cms_control_classes(list(INPUT_CLASSES)))


class CmsAdminTextareaWidget(AdminTextareaWidget):
    def __init__(self, attrs=None):
        super().__init__(attrs)
        self.attrs['class'] = ' '.join(cms_control_classes(list(TEXTAREA_CLASSES)))


def apply_readable_widget(field):
    widget = field.widget
    if isinstance(widget, (CheckboxInput, Select, FileInput, TinyMCE)):
        return field
    if isinstance(widget, Textarea):
        field.widget = CmsAdminTextareaWidget(attrs=widget.attrs)
    elif isinstance(widget, (TextInput, AdminTextInputWidget)):
        field.widget = CmsAdminTextInputWidget(attrs=widget.attrs)
    return field
