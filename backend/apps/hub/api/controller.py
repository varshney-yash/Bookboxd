from django.views.generic import TemplateView, CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import requests
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from hub.models import *
from django.db.models import Count

class HomeView(TemplateView):
    template_name = 'hub/home.html'
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

@login_required
@require_POST
def create_list(request):
    name = request.POST.get('name')
    if name:
        book_list = BookList.objects.create(name=name, user=request.user)
        return JsonResponse({'success': True, 'id': book_list.id, 'name': book_list.name})
    else:
        return JsonResponse({'success': False, 'error': 'List name is required'})
    
@login_required
def manage_lists(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            BookList.objects.create(name=name, user=request.user)
        return redirect('manage_lists')

    user_lists = BookList.objects.filter(user=request.user).annotate(book_count=Count('listbook'))
    return render(request, 'hub/manage_list.html', {'user_lists': user_lists})

@login_required
@require_POST
def delete_list(request):
    list_id = request.POST.get('list_id')
    try:
        book_list = BookList.objects.get(id=list_id, user=request.user)
        book_list.delete()
        return JsonResponse({'success': True})
    except BookList.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'List not found'})

@login_required
@require_POST
def add_to_list(request):
    book_id = request.POST.get('book_id')
    list_ids = request.POST.getlist('list_ids[]')
    if not book_id or not list_ids:
        return JsonResponse({'success': False, 'error': 'Missing book_id or list_ids'})

    try:
        user_lists = BookList.objects.filter(user=request.user)
        for list in user_lists:
            if str(list.id) in list_ids:
                ListBook.objects.get_or_create(book_list=list, google_books_id=book_id)
            else:
                ListBook.objects.filter(book_list=list, google_books_id=book_id).delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}) 

def explore_lists(request):
    all_lists = BookList.objects.annotate(book_count=Count('listbook')).select_related('user').order_by('-created_at')
    
    context = {
        'all_lists': all_lists
    }
    return render(request, 'hub/explore.html', context)

@login_required
def get_user_lists(request):
    book_id = request.GET.get('book_id')
    user_lists = BookList.objects.filter(user=request.user)
    
    lists_data = []
    for list in user_lists:
        has_book = ListBook.objects.filter(book_list=list, google_books_id=book_id).exists() if book_id else False
        lists_data.append({
            'id': list.id,
            'name': list.name,
            'has_book': has_book
        })
    
    return JsonResponse({'lists': lists_data})

    
class RegisterView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'hub/register.html'

class CustomLoginView(LoginView):
    template_name = 'hub/login.html' 
    next_page = '/'

class CustomLogoutView(LogoutView):
    next_page = '/'