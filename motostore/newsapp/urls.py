from django.urls import path
from newsapp import views

app_name = 'newsapp'

urlpatterns = [
    path('', views.NewsView.as_view(), name='index_news'),
]