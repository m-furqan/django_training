import imp
from django.urls import path

from products.views import HomePageView, CategoryDetailView, ProductDetailView


app_name = 'products'
urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('<int:pk>/category/', CategoryDetailView.as_view(), name='category'),
    path('<int:pk>/product/', ProductDetailView.as_view(), name='product'),
]
