from django.views.generic import TemplateView, CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import requests
import os

class HomeView(TemplateView):
    pass

class RegisterView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'hub/register.html'

class CustomLoginView(LoginView):
    template_name = 'hub/login.html' 
    next_page = '/'

class CustomLogoutView(LogoutView):
    next_page = '/'