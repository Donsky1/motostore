from rest_framework import viewsets

from .models import Marks, Moto_models, Moto_type
from .serializers import MarkSerializer, MotorcycleModelsSerializer, MotorcycleTypesSerializer


class MarkViewSet(viewsets.ModelViewSet):
    queryset = Marks.objects.all()
    serializer_class = MarkSerializer


class MotorcycleModelsViewSet(viewsets.ModelViewSet):
    queryset = Moto_models.objects.all()
    serializer_class = MotorcycleModelsSerializer


class MotorcycleTypesViewSet(viewsets.ModelViewSet):
    queryset = Moto_type.objects.all()
    serializer_class = MotorcycleTypesSerializer