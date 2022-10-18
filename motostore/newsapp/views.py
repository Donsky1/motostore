from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from .models import News
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .forms import CreateNewsForm


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
    form_class = CreateNewsForm
    success_url = reverse_lazy('news_app:index_news')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(CreateNewsView, self).form_valid(form)


class UpdateNewsView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    template_name = 'newsapp/update-news.html'
    form_class = CreateNewsForm
    model = News
    permission_denied_message = 'Вы не можете редактировать эту новость'

    def test_func(self):
        cur_news = News.objects.get(pk=self.kwargs['pk'])
        return self.request.user.id == cur_news.author.id


class NewsDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = News
    success_url = reverse_lazy('news_app:index_news')
    template_name = 'delete-confirm.html'

    def test_func(self):
        cur_obj = News.objects.get(pk=self.kwargs['pk'])
        return self.request.user.id == cur_obj.author.id