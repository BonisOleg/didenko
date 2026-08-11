"""Admin mixins for Unfold CMS."""

from django.http import HttpResponseRedirect
from django.urls import reverse


class SingletonModelAdminMixin:
    change_url_name: str = ''

    def has_add_permission(self, request) -> bool:
        return False

    def has_delete_permission(self, request, obj=None) -> bool:
        return False

    def changelist_view(self, request, extra_context=None):
        return HttpResponseRedirect(reverse(self.change_url_name, args=[1]))


class ContentSectionAdminMixin(SingletonModelAdminMixin):
    page_slug: str = ''
    section_slug: str = ''

    def changelist_view(self, request, extra_context=None):
        from src.pages.admin_site_content import site_content_section_view

        return site_content_section_view(
            request,
            self.page_slug,
            self.section_slug,
            model_admin=self,
        )

    def change_view(self, request, object_id, form_url='', extra_context=None):
        from src.pages.admin_site_content import site_content_section_view

        return site_content_section_view(
            request,
            self.page_slug,
            self.section_slug,
            model_admin=self,
        )

    def has_module_permission(self, request) -> bool:
        return request.user.is_staff

    def has_view_permission(self, request, obj=None) -> bool:
        return request.user.is_staff

    def has_change_permission(self, request, obj=None) -> bool:
        return request.user.is_staff
