from django.http import Http404
from django.shortcuts import render
from django.views.generic import TemplateView, View

from src.leads.forms import LeadForm
from src.leads.models import Lead
from src.pages.selectors import (
    get_home_context,
    get_published_page,
    get_site_settings,
    resolve_page_seo,
)


class HomeView(TemplateView):
    template_name = 'pages/home.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(get_home_context())
        ctx['lead_form'] = LeadForm(source=Lead.Source.HOME)
        return ctx


class PageDetailView(View):
    template_name = 'pages/page_detail.html'
    about_template_name = 'pages/about.html'

    def get(self, request, slug):
        page = get_published_page(slug)
        if page is None:
            raise Http404
        ctx = {'page': page, **resolve_page_seo(page)}
        if slug == 'pro-nas':
            from src.pages.about_body_render import render_about_body_html

            ctx['lead_form'] = LeadForm(source=Lead.Source.HOME)
            ctx['about_body_html'] = render_about_body_html(page)
            return render(request, self.about_template_name, ctx)
        return render(request, self.template_name, ctx)


class ContactsView(View):
    template_name = 'pages/contacts.html'

    def get(self, request):
        page = get_published_page('kontakty')
        if page is None:
            raise Http404
        ctx = {
            'page': page,
            'site_settings': get_site_settings(),
            'lead_form': LeadForm(source=Lead.Source.CONTACTS),
            **resolve_page_seo(page),
        }
        return render(request, self.template_name, ctx)
