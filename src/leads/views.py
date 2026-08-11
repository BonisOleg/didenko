from django.shortcuts import render
from django.views.decorators.http import require_POST

from src.leads.forms import LeadForm
from src.leads.models import Lead
from src.leads.services import submit_lead


@require_POST
def lead_submit(request):
    if request.POST.get('honeypot'):
        return render(request, 'leads/partials/success.html', status=200)

    source = request.POST.get('source') or Lead.Source.HOME
    if source not in Lead.Source.values:
        source = Lead.Source.HOME

    prefix = request.POST.get('form_prefix') or None
    form = LeadForm(request.POST, source=source, prefix=prefix)
    if form.is_valid():
        submit_lead(
            name=form.cleaned_data['name'],
            phone=form.cleaned_data['phone'],
            email=form.cleaned_data['email'],
            consent=form.cleaned_data['consent'],
            source=source,
            source_url=request.META.get('HTTP_REFERER', request.path)[:512],
            service=form.cleaned_data.get('service'),
            selected_topics=form.cleaned_data.get('selected_topics') or [],
        )
        return render(request, 'leads/partials/success.html', status=200)

    return render(
        request,
        'leads/partials/form.html',
        {'lead_form': form, 'source': source},
        status=422,
    )
