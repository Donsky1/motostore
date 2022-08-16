from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def news(request, value):
    print(request)
    print(value)
    return HttpResponse(f'Hello, motorcycles store | {value}')