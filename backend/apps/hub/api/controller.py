from django.views.generic import TemplateView, CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import requests
from django.conf import settings

class HomeView(TemplateView):
    template_name = 'hub/book_list.html'
    items_per_page = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        query = self.request.GET.get('q', '')
        sort = self.request.GET.get('sort', 'relevance')  
        page = self.request.GET.get('page', 1)
        
        if query:
            api_key = settings.GOOGLE_API_KEY
            url = f'https://www.googleapis.com/books/v1/volumes?q={query}&orderBy={sort}&key={api_key}&maxResults=40'
            
            response = requests.get(url)
            if response.status_code == 200:
                books_data = response.json().get('items', [])
                books = []
                for book in books_data:
                    volume_info = book.get('volumeInfo', {})
                    books.append({
                        'google_books_id': book.get('id'),
                        'title': volume_info.get('title', 'No title'),
                        'authors': volume_info.get('authors', ['Unknown']),
                        'description': volume_info.get('description', 'No description available'),
                        'thumbnail': volume_info.get('imageLinks', {}).get('thumbnail', ''),
                        'published_date': volume_info.get('publishedDate', 'Unknown'),
                    })
                
                paginator = Paginator(books, self.items_per_page)
                try:
                    books_page = paginator.page(page)
                except PageNotAnInteger:
                    books_page = paginator.page(1)
                except EmptyPage:
                    books_page = paginator.page(paginator.num_pages)

                context['books'] = books_page
                context['total_results'] = len(books)
            else:
                context['error'] = 'Failed to fetch books from Google Books API'
        
        context['query'] = query
        context['current_sort'] = sort
        return context

class RegisterView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'hub/register.html'

class CustomLoginView(LoginView):
    template_name = 'hub/login.html' 
    next_page = '/'

class CustomLogoutView(LogoutView):
    next_page = '/'