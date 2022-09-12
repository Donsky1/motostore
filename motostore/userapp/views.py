from django.contrib.auth import views as auth_views
from .forms import UserLoginForm, StoreAppUserCreatingForm
from django.views import generic
from .models import StoreAppUser
from django.urls import reverse_lazy
from django.shortcuts import redirect
from storeapp.models import Motorcycle
from newsapp.models import News


# Create your views here.
class UserLoginView(auth_views.LoginView):
    template_name = 'userapp/login.html'
    form_class = UserLoginForm
    redirect_authenticated_user = reverse_lazy('store_app:index')


class RegistrationView(generic.CreateView):
    model = StoreAppUser
    template_name = 'userapp/registarion.html'
    form_class = StoreAppUserCreatingForm
    success_url = reverse_lazy('store_app:index')

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('store_app:index')
        return super(RegistrationView, self).get(request, *args, **kwargs)


class ProfileView(generic.DetailView):
    template_name = 'userapp/profile.html'
    model = StoreAppUser

    def get_context_data(self, **kwargs):
        user = StoreAppUser.objects.get(pk=self.kwargs['pk'])
        context = super(ProfileView, self).get_context_data(**kwargs)
        context['offers'] = Motorcycle.objects.filter(user=user)
        context['news'] = News.objects.filter(author=user)
        return context