from django.shortcuts import render
from django.views import generic


# Create your views here.
class NewsView(generic.TemplateView):
    template_name = 'newsapp/index-news.html'