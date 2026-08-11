"""TinyMCE для Unfold: HTMLField не підміняється звичайним textarea."""

from tinymce.models import HTMLField
from tinymce.widgets import AdminTinyMCE


class TinyMCEAdminMixin:
    """Підключати перед unfold.admin.ModelAdmin."""

    formfield_overrides = {
        HTMLField: {'widget': AdminTinyMCE},
    }
