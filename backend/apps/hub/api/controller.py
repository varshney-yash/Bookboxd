from django.views.generic import TemplateView, CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import requests
from django.conf import settings
from django.shortcuts import render, redirect

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
    
def book_detail(request, google_books_id):
    api_key = settings.GOOGLE_API_KEY
    url = f'https://www.googleapis.com/books/v1/volumes/{google_books_id}?key={api_key}'
    
    response = requests.get(url)
    if response.status_code == 200:
        book_data = response.json()
        volume_info = book_data.get('volumeInfo', {})
        
        book = {
            'google_books_id': google_books_id,
            'title': volume_info.get('title', 'No title'),
            'subtitle': volume_info.get('subtitle', ''),
            'authors': volume_info.get('authors', ['Unknown']),
            'description': volume_info.get('description', 'No description available'),
            'thumbnail': volume_info.get('imageLinks', {}).get('thumbnail', ''),
            'published_date': volume_info.get('publishedDate', 'Unknown'),
            'publisher': volume_info.get('publisher', ''),
            'categories': volume_info.get('categories', []),
            'page_count': volume_info.get('pageCount', 'Unknown'),
            'language': volume_info.get('language', 'Unknown'),
            'preview_link': volume_info.get('previewLink', '#'),
            'average_rating': volume_info.get('averageRating', None),
            'ratings_count': volume_info.get('ratingsCount', 0),
            'isbn_10': next((id['identifier'] for id in volume_info.get('industryIdentifiers', []) if id['type'] == 'ISBN_10'), None),
            'isbn_13': next((id['identifier'] for id in volume_info.get('industryIdentifiers', []) if id['type'] == 'ISBN_13'), None),
            'table_of_contents': volume_info.get('tableOfContents', []),
            'maturity_rating': volume_info.get('maturityRating', 'Not available'),
        }
        
        context = {'book': book}
        return render(request, 'hub/book_detail.html', context)
    else:
        context = {'error': 'Book not found'}
        return render(request, 'hub/book_detail.html', context)


class RegisterView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'hub/register.html'

class CustomLoginView(LoginView):
    template_name = 'hub/login.html' 
    next_page = '/'

class CustomLogoutView(LogoutView):
    next_page = '/'