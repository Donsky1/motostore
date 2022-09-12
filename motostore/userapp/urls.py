from django.urls import path
from django.contrib.auth.views import LogoutView

from . import views

app_name = 'userapp'

urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('registration/', views.RegistrationView.as_view(), name='registration'),
    path('profile/<int:pk>', views.ProfileView.as_view(), name='profile'),
]