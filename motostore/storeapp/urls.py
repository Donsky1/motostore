from django.urls import path


from . import views

app_name = 'store_app'

urlpatterns = [
        path('', views.IndexView.as_view(), name='index'),
        path('motorcycle/<int:pk>', views.MotorcycleDetailView.as_view(), name='motorcycle_detail'),
        path('about/', views.AboutView.as_view(), name='about'),
        path('contact/', views.ContactView.as_view(), name='contact'),
        path('terms/', views.TermsView.as_view(), name='terms'),
        path('motorcycles/<str:tag>', views.TypeMotoView.as_view(), name='type-motorcycles'),
        path('motorcycles-filter/', views.MotorcyclesFilterView.as_view(), name='filter-motorcycles'),
        path('search/', views.SearchView.as_view(), name='search'),
        path('create-offer/', views.CreateOfferView.as_view(), name='create-offer'),
        path('motorcycles-filter/<str:user>', views.MotorcyclesFilterUserView.as_view(), name='motorcycle-filter-user'),
]