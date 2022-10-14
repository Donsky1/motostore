from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views import generic
from django.http import HttpResponseRedirect, HttpResponseForbidden

from .forms import MotorcycleForm, MotorcycleImagesInlineFormSet, MotorcycleImagesInlineFormCreateSet
from .models import Motorcycle, Moto_models, Moto_type, City, Marks, Color, Motorcycle_images
from django.db.models import Q
from functools import wraps


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
            result = result.select_related('mark_info', 'model_info', 'color', 'moto_type', 'city'). \
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


class MotorcyclesFilterUserView(MotorcyclesView):
    template_name = 'storeapp/index.html'

    def get_queryset(self):
        user = self.kwargs.get('user')
        response = Motorcycle.objects.all()
        if user:
            response = response.filter(user__username=user)
        return response


def owner_required(view):
    '''Декоратор для проверки правомерности изменения объявления.
    Только владелец объявления может вносить изменения'''
    @wraps(view)
    def wrapper(*args, **kwargs):
        request = args[0]
        id_offer = args[0].path.split('/')[2]
        cur_offer = Motorcycle.objects.get(pk=id_offer)
        if request.user.id == cur_offer.user.id:
            return view(*args, **kwargs)
        else:
            return HttpResponseRedirect(reverse_lazy('store_app:index'))
    return wrapper


@login_required
@owner_required
def update_offer(request, pk):
    obj_offer = Motorcycle.objects.get(pk=pk)
    if request.method == 'POST':
        form = MotorcycleForm(request.POST, request.FILES, instance=obj_offer)
        image_formset = MotorcycleImagesInlineFormSet(request.POST, request.FILES, instance=obj_offer)
        if image_formset.is_valid() and form.is_valid():
            form.save()
            image_formset.save()
            return HttpResponseRedirect(reverse_lazy('user_app:profile', kwargs={'pk': request.user.id}))
    else:
        form = MotorcycleForm(instance=obj_offer)
        image_formset = MotorcycleImagesInlineFormSet(instance=obj_offer)
    return render(request, 'storeapp/update_offer.html', {'image_formset': image_formset,
                                                          'form': form})


@login_required
def create_offer(request):
    if request.method == 'POST':
        form = MotorcycleForm(request.POST, request.FILES)
        image_formset = MotorcycleImagesInlineFormCreateSet(request.POST, request.FILES)
        if image_formset.is_valid() and form.is_valid():
            offer = form.save()
            instances = image_formset.save(commit=False)
            for instance in instances:
                instance.moto_id = offer.id
                instance.save()
            image_formset.save_m2m()
            return HttpResponseRedirect(reverse_lazy('user_app:profile', kwargs={'pk': request.user.id}))
    else:
        form = MotorcycleForm()
        image_formset = MotorcycleImagesInlineFormCreateSet()
    return render(request, 'storeapp/create-offer.html', {'image_formset': image_formset,
                                                          'form': form})


class MotorcycleDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Motorcycle
    success_url = reverse_lazy('store_app:index')
    template_name = 'delete-confirm.html'

    def test_func(self):
        cur_obj = Motorcycle.objects.get(pk=self.kwargs['pk'])
        return self.request.user.id == cur_obj.user.id