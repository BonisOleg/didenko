from django.http import Http404
from django.shortcuts import render
from django.views import View

from src.leads.forms import LeadForm
from src.leads.models import Lead
from src.services.selectors import (
    get_published_service,
    list_published_services,
    resolve_service_seo,
)


class ServiceListView(View):
    template_name = 'services/list.html'

    def get(self, request):
        from src.services.models import ProcessStep

        services = list_published_services()
        form = LeadForm(source=Lead.Source.SERVICE)
        process_steps = ProcessStep.objects.filter(is_active=True).order_by(
            'sort_order',
            'id',
        )
        return render(
            request,
            self.template_name,
            {
                'services': services,
                'process_steps': process_steps,
                'lead_form': form,
                'page_title': 'Послуги',
                'seo_title': 'Послуги арбітражної керуючої Діденко',
                'seo_description': (
                    'Повний спектр послуг у справах про банкрутство фізичних осіб: '
                    'консультації, аналіз, підготовка документів і супровід процедури.'
                ),
                'seo_h1': 'Послуги',
            },
        )


class ServiceDetailView(View):
    template_name = 'services/detail.html'
    partial_template_name = 'services/partials/modal_detail.html'

    def get(self, request, slug):
        service = get_published_service(slug)
        if service is None:
            raise Http404
        form = LeadForm(
            source=Lead.Source.SERVICE,
            initial={'service': service.pk},
        )
        ctx = {
            'service': service,
            'lead_form': form,
            **resolve_service_seo(service),
        }
        template = (
            self.partial_template_name
            if getattr(request, 'htmx', False)
            else self.template_name
        )
        return render(request, template, ctx)
