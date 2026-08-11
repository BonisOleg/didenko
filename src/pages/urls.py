from django.urls import path

from src.pages.views import ContactsView, HomeView, PageDetailView

app_name = 'pages'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('kontakty/', ContactsView.as_view(), name='contacts'),
    path('<slug:slug>/', PageDetailView.as_view(), name='page_detail'),
]
