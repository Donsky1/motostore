from django.shortcuts import render
from django.views import generic
from .models import News
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
class NewsView(generic.ListView):
    model = News
    template_name = 'newsapp/index-news.html'
    context_object_name = 'news'


class NewsDetailView(generic.DetailView):
    model = News
    template_name = 'newsapp/news-detail.html'


class CreateNewsView(LoginRequiredMixin, generic.CreateView):
    template_name = 'newsapp/create-news.html'
    model = News
    fields = '__all__'