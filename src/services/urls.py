from django.urls import path

from src.services.views import ServiceDetailView, ServiceListView

app_name = 'services'

urlpatterns = [
    path('posluhy/', ServiceListView.as_view(), name='list'),
    path('posluhy/<slug:slug>/', ServiceDetailView.as_view(), name='detail'),
]
