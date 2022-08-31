from django.shortcuts import render
from django.views import generic
from .models import Motorcycle


class IndexView(generic.ListView):
    model = Motorcycle
    template_name = 'storeapp/index.html'
    context_object_name = 'motorcycles'


class MotorcycleDetailView(generic.DetailView):
    model = Motorcycle
    template_name = 'storeapp/moto-detail.html'


class AboutView(generic.TemplateView):
    template_name = 'storeapp/about.html'


class ContactView(generic.TemplateView):
    template_name = 'storeapp/contact.html'


class TermsView(generic.TemplateView):
    template_name = 'storeapp/terms-conditions.html'