from django.urls import path

from src.leads.views import lead_submit

app_name = 'leads'

urlpatterns = [
    path('leads/submit/', lead_submit, name='submit'),
]
