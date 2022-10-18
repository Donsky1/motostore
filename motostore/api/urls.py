from django.urls import path, include
from django.views import generic

from . import views
from rest_framework import routers

from .views import MarksViewSet, MotorcycleModelsViewSet, MotorcycleTypesViewSet, CityViewSet, MotorcycleViewSet, NewsViewSet

router = routers.DefaultRouter()
router.register('marks', MarksViewSet)
router.register('motorcycle-models', MotorcycleModelsViewSet)
router.register('motorcycle-types', MotorcycleTypesViewSet)
router.register('cities', CityViewSet)
router.register('motorcycles', MotorcycleViewSet)
router.register('news', NewsViewSet)

app_name = 'api_v0'

urlpatterns = [
    path('', include(router.urls)),

]


