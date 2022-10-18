from functools import wraps
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from .models import Motorcycle


def owner_required(view):
    ''' Декоратор для проверки правомерности изменения объявления.
    Только владелец объявления может вносить изменения. '''

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
