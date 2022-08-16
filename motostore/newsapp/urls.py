from django.urls import path
from newsapp import views

app_name = 'newsapp'

urlpatterns = [
    path('<str:value>/', views.news, name='news'),
]