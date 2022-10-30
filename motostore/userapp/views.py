from django.contrib.auth import views as auth_views
from rest_framework.authtoken.models import Token
from django.views import generic
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm, UserChangeForm

from storeapp.models import Motorcycle
from newsapp.models import News
from .models import StoreAppUser
from .forms import UserLoginForm, StoreAppUserCreatingForm


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


def generate_token_ajax(request):
    user = request.user
    try:
        user.auth_token.delete()
        token = Token.objects.create(user=user)
    except Exception as err:
        token = Token.objects.create(user=user)
    return JsonResponse({'key': token.key})


def change_password(request):
    user = request.user
    object = StoreAppUser.objects.get(pk=user.pk)
    offers = Motorcycle.objects.filter(user=user)
    news = News.objects.filter(author=user)

    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Вы успешно обновили пароль!')
            return HttpResponseRedirect(reverse_lazy('store_app:index'))
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибку ниже.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'userapp/profile_change_password.html', {
        'form': form, 'object': object, 'offers': offers, 'news': news
    })


class ProfileUpdateView(generic.UpdateView):
    model = StoreAppUser
    fields = ('username', 'email', 'first_name', 'last_name', 'email', 'phone', 'telegram_account', 'text')
    template_name = 'userapp/profile_update.html'
    success_url = reverse_lazy('store_app:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['offers'] = Motorcycle.objects.filter(user=self.request.user)
        context['news'] = News.objects.filter(author=self.request.user)
        return context
