from django.urls import path
from newsapp import views

app_name = 'newsapp'

urlpatterns = [
    path('', views.NewsView.as_view(), name='index_news'),
    path('article/<int:pk>', views.NewsDetailView.as_view(), name='news_detail'),
    path('create-news/', views.CreateNewsView.as_view(), name='create_news'),
    path('update-news/<int:pk>', views.UpdateNewsView.as_view(), name='update_news'),
    path('delete-news/<int:pk>', views.NewsDeleteView.as_view(), name='delete_news'),
]