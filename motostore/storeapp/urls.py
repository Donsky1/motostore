from django.urls import path, include
from django.views import generic

from . import views
# from rest_framework import routers
#
# from storeapp.api_views import MarkViewSet, MotorcycleModelsViewSet, MotorcycleTypesViewSet
#
# router = routers.DefaultRouter()
# router.register(r'marks', MarkViewSet)
# router.register(r'motorcycle-models', MotorcycleModelsViewSet)
# router.register(r'motorcycle-types', MotorcycleTypesViewSet)

app_name = 'store_app'

urlpatterns = [
        path('', views.IndexView.as_view(), name='index'),
        path('motorcycle/<int:pk>', views.MotorcycleDetailView.as_view(), name='motorcycle_detail'),
        path('about/', generic.TemplateView.as_view(template_name='storeapp/about.html'), name='about'),
        path('terms/', generic.TemplateView.as_view(template_name='storeapp/terms-conditions.html'), name='terms'),
        path('contact/', views.ContactView.as_view(), name='contact'),
        path('motorcycles/<str:tag>', views.TypeMotorcycleView.as_view(), name='type-motorcycles'),
        path('motorcycles-filter/', views.MotorcyclesFilterView.as_view(), name='filter-motorcycles'),
        path('search/', views.SearchView.as_view(), name='search'),
        path('create-offer/', views.create_offer, name='create-offer'),
        path('update-offer/<int:pk>', views.update_offer, name='update-offer'),
        path('delete-offer/<int:pk>', views.MotorcycleDeleteView.as_view(), name='delete-offer'),
        path('motorcycles-filter/<str:user>', views.MotorcyclesFilterUserView.as_view(), name='motorcycle-filter-user'),
        path('get-model-filter/', views.get_filter_model_ajax),
]


