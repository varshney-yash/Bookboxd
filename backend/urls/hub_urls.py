from django.urls import path
from backend.apps.hub.api import controller as hub_api_views
from django.views.generic.base import RedirectView

hub_paths = [
    path('', RedirectView.as_view(url='/home/', permanent=True)),
    path('home/', hub_api_views.HomeView, name='book_list')
]