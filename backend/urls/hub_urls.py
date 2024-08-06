from django.urls import path
from backend.apps.hub.api import controller as hub_api_views
from django.views.generic.base import RedirectView

hub_paths = [
    path('', RedirectView.as_view(url='/home/', permanent=True)),
    path('home/', hub_api_views.HomeView.as_view(), name='home'),
    path('book/<str:google_books_id>', hub_api_views.book_detail, name='book_detail'),
    path('register/', hub_api_views.RegisterView.as_view(), name='register'),
    path('login/', hub_api_views.CustomLoginView.as_view(), name='login'),
    path('logout/', hub_api_views.CustomLogoutView.as_view(), name='logout'),
    path('manage-lists/', hub_api_views.manage_lists, name='manage_lists'),
    path('delete-list/', hub_api_views.delete_list, name='delete_list'),
    path('create-list/', hub_api_views.create_list, name='create_list'),
    path('explore/', hub_api_views.explore_lists, name='explore_lists'),
    path('list/<int:list_id>', hub_api_views.list_detail, name='list_detail'),
    path('get-user-lists/', hub_api_views.get_user_lists, name='get_user_lists'),
    path('add-to-list/', hub_api_views.add_to_list, name='add_to_list'),
    path('like-list/<int:list_id>/', hub_api_views.like_list, name='like_list'),
    path('health/', hub_api_views.ping, name='ping')
]