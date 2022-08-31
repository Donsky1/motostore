from django.urls import path

from . import views

app_name = 'store_app'

urlpatterns = [
        path('', views.IndexView.as_view(), name='index'),
        path('motorcycle/<int:pk>', views.MotorcycleDetailView.as_view(), name='motorcycle_detail'),
        path('about/', views.AboutView.as_view(), name='about'),
        path('contact/', views.ContactView.as_view(), name='contact'),
        path('terms/', views.TermsView.as_view(), name='terms'),
]