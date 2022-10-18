from rest_framework import viewsets


from storeapp.models import Marks, Moto_models, Moto_type, City, Motorcycle
from newsapp.models import News
from .serializers import MarkSerializer, MotorcycleModelsSerializer, MotorcycleTypesSerializer, CitySerializer, MotorcycleSerializer, NewsSerializer
from .permissions import ReadOnly


class MotorcycleModelsViewSet(viewsets.ModelViewSet):
    queryset = Moto_models.objects.all()
    serializer_class = MotorcycleModelsSerializer


class MotorcycleTypesViewSet(viewsets.ModelViewSet):
    queryset = Moto_type.objects.all()
    serializer_class = MotorcycleTypesSerializer


class MarksViewSet(viewsets.ModelViewSet):
    queryset = Marks.objects.all()
    serializer_class = MarkSerializer


class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer


class MotorcycleViewSet(viewsets.ModelViewSet):
    queryset = Motorcycle.active_offer.all().order_by('created_at')
    serializer_class = MotorcycleSerializer
    permission_classes = [ReadOnly]


class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer