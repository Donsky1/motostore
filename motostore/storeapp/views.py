from django.shortcuts import render
from django.views import generic
from .models import Motorcycle, Moto_models, Moto_type


class MotorcycleTypesMixin(generic.ListView):
    model = Motorcycle
    context_object_name = 'motorcycles'
    ordering = ['-created_at']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['moto_types'] = Moto_type.objects.all()
        return context


class IndexView(MotorcycleTypesMixin):
    template_name = 'storeapp/index.html'


class TypeMotoView(MotorcycleTypesMixin):
    template_name = 'storeapp/typemoto.html'
    allow_empty = False

    def get_queryset(self):
        tag = self.kwargs['tag']
        return Motorcycle.objects.filter(moto_type__name=tag)


class MotorcycleDetailView(generic.DetailView):
    model = Motorcycle
    template_name = 'storeapp/moto-detail.html'

    def get_object(self, queryset=None):
        post = Motorcycle.objects.get(pk=self.kwargs['pk'])
        post.rate += 1
        post.save()
        return super(MotorcycleDetailView, self).get_object()


class AboutView(generic.TemplateView):
    template_name = 'storeapp/about.html'


class ContactView(generic.TemplateView):
    template_name = 'storeapp/contact.html'


class TermsView(generic.TemplateView):
    template_name = 'storeapp/terms-conditions.html'


class TestView(generic.ListView):
    model = Moto_models
    template_name = 'storeapp/test.html'
    context_object_name = 'models'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['name'] = 'TEST CONTEXT'
        context['motorcycles'] = Motorcycle.objects.all()
        return context