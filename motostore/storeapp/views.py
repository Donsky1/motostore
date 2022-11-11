from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views import generic
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, Http404
from django.db.models import Q
import json

from .forms import MotorcycleForm, MotorcycleImagesInlineFormSet, MotorcycleImagesInlineFormCreateSet, ContactForm
from .models import Motorcycle, Moto_models, Moto_type, City, Marks, Color
from .decorators import owner_required
from .serializers import MotorcycleModelsSerializer


class MotorcyclesView(generic.ListView):
    model = Motorcycle
    context_object_name = 'motorcycles'
    ordering = ['-created_at']
    queryset = Motorcycle.active_offer.all()
    paginate_by = 7
    template_name = 'storeapp/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['moto_types'] = Moto_type.objects.all()
        context['marks'] = {motorcycle.mark_info for motorcycle in self.queryset}
        return context


class IndexView(MotorcyclesView):
    pass


class TypeMotorcycleView(MotorcyclesView):
    allow_empty = False

    def get_queryset(self):
        tag = self.kwargs['tag']
        return self.queryset.filter(moto_type__name=tag)


class MotorcycleDetailView(generic.DetailView):
    model = Motorcycle
    template_name = 'storeapp/moto-detail.html'

    def get_object(self, queryset=None):
        post = get_object_or_404(Motorcycle, pk=self.kwargs['pk'])
        post.rate += 1
        post.save()
        return super(MotorcycleDetailView, self).get_object()


class ContactView(generic.FormView):
    form_class = ContactForm
    template_name = 'storeapp/contact.html'
    success_url = reverse_lazy('store_app:contact')

    # TODO send "mail"
    def send_message_to(self, name, email, message):
        print(f'''
        Уведомление с формы:
        -------------------
        Пользователь: {name}
        Почта: {email}
        Сообщение: {message}
''')

    def form_valid(self, form):
        name = form.cleaned_data['your_name']
        email = form.cleaned_data['email']
        message = form.cleaned_data['message']
        self.send_message_to(name, email, message)
        return super(ContactView, self).form_valid(form)


class SearchView(MotorcyclesView):

    def get_queryset(self):
        q = self.request.GET.get('q')
        if q:
            return self.queryset.select_related('mark_info', 'model_info', 'color', 'moto_type', 'city'). \
                filter(Q(mark_info__name__icontains=q) |
                       Q(model_info__name__icontains=q) |
                       Q(color__name__icontains=q) |
                       Q(moto_type__name__icontains=q) |
                       Q(city__name__icontains=q) |
                       Q(comment__icontains=q))
        else:
            return self.queryset


class MotorcyclesFilterView(MotorcyclesView):

    def get_queryset(self):
        # filtering block
        mark = self.request.GET.get('mark')
        model_name = self.request.GET.get('model')
        moto_type = self.request.GET.get('moto_type')
        price_from = self.request.GET.get('price_from')
        price_to = self.request.GET.get('price_to')

        response = self.queryset
        if mark:
            response = response.filter(mark_info__name=mark)
        if model_name:
            response = response.filter(model_info__name=model_name)
        if moto_type:
            response = response.filter(moto_type__name=moto_type)
        if price_from:
            response = response.filter(price__gte=price_from)
        if price_to:
            response = response.filter(price__lte=price_to)
        return response


class MotorcyclesFilterUserView(MotorcyclesView):

    def get_queryset(self):
        user = self.kwargs.get('user')
        response = self.queryset
        if user:
            response = response.filter(user__username=user)
        return response


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
            return HttpResponseRedirect(reverse_lazy('store_app:motorcycle_detail', kwargs={'pk': pk}))
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
            offer = form.save(commit=False)
            offer.user = request.user
            offer.save()
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


def get_filter_model_ajax(request):
    mark = request.GET.get('selected_mark')
    motorcycles = Motorcycle.active_offer.select_related('model_info', 'mark_info').filter(mark_info__name=mark)
    models = {motorcycle.model_info for motorcycle in motorcycles}
    serializer = MotorcycleModelsSerializer(models, many=True)
    return JsonResponse(serializer.data, safe=False)


def subscription(request):
    email = request.POST.get('email_subscription')
    print('Новый подписчик: ', email)
    return HttpResponseRedirect(reverse_lazy('store_app:index'))