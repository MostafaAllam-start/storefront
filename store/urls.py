from django.urls import path
from .views import ProductList, ProductDetail, collection_list, collection_detail
urlpatterns = [
    path('product/', ProductList.as_view(), name='product-list'),
    path('product/<int:pk>/', ProductDetail.as_view(), name='product-detail'),
    path('collection/', collection_list, name='collection-list'),
    path('collection/<int:pk>/', collection_detail, name='collection-detail')

]
