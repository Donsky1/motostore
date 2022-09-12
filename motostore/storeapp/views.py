from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from .models import Motorcycle, Moto_models, Moto_type, City, Marks, Color
from django.db.models import Q


class MotorcyclesView(generic.ListView):
    model = Motorcycle
    context_object_name = 'motorcycles'
    ordering = ['-created_at']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['moto_types'] = Moto_type.objects.all()
        context['cities'] = City.objects.all()
        context['marks'] = Marks.objects.all()
        context['models'] = Moto_models.objects.all()
        context['colors'] = Color.objects.all()
        return context


class IndexView(MotorcyclesView):
    template_name = 'storeapp/index.html'


class TypeMotoView(MotorcyclesView):
    template_name = 'storeapp/index.html'
    allow_empty = False

    def get_queryset(self):
        tag = self.kwargs['tag']
        return Motorcycle.objects.filter(moto_type__name=tag)


class MotorcycleDetailView(generic.DetailView):
    model = Motorcycle
    template_name = 'storeapp/moto-detail.html'

    def get_object(self, queryset=None):
        post = get_object_or_404(Motorcycle, pk=self.kwargs['pk'])
        post.rate += 1
        post.save()
        return super(MotorcycleDetailView, self).get_object()


class AboutView(generic.TemplateView):
    template_name = 'storeapp/about.html'


class ContactView(generic.TemplateView):
    template_name = 'storeapp/contact.html'


class TermsView(generic.TemplateView):
    template_name = 'storeapp/terms-conditions.html'


class SearchView(MotorcyclesView):
    template_name = 'storeapp/index.html'

    def get_queryset(self):
        result = Motorcycle.objects.all()
        q = self.request.GET.get('q')
        if q:
            result = result.select_related('mark_info').\
                select_related('model_info').\
                select_related('color'). \
                select_related('moto_type'). \
                select_related('city'). \
                filter(Q(mark_info__name__icontains=q) |
                       Q(model_info__name__icontains=q) |
                       Q(color__name__icontains=q) |
                       Q(moto_type__name__icontains=q) |
                       Q(city__name__icontains=q) |
                       Q(comment__icontains=q))

        return result


class MotorcyclesFilterView(MotorcyclesView):
    template_name = 'storeapp/index.html'

    def get_queryset(self):
        city = self.request.GET.get('city')
        mark = self.request.GET.get('mark')
        model = self.request.GET.get('model')
        color = self.request.GET.get('color')
        price_from = self.request.GET.get('price_from')
        price_to = self.request.GET.get('price_to')
        response = Motorcycle.objects.all()
        if city:
            response = response.filter(city__name=city)
        if mark:
            response = response.filter(mark_info__name=mark)
        if model:
            response = response.filter(model_info__name=model)
        if color:
            response = response.filter(color__name=color)
        if price_from:
            response = response.filter(price__gte=price_from)
        if price_to:
            response = response.filter(price__lte=price_to)
        return response


class CreateOfferView(LoginRequiredMixin, generic.CreateView):
    model = Motorcycle
    fields = '__all__'
    template_name = 'storeapp/create-offer.html'


class MotorcyclesFilterUserView(MotorcyclesView):
    template_name = 'storeapp/index.html'

    def get_queryset(self):
        user = self.kwargs.get('user')
        response = Motorcycle.objects.all()
        if user:
            response = response.filter(user__username=user)
        return response