from django.urls import path
from .views import product_list, product_detail, collection_list, collection_detail
urlpatterns = [
    path('product/', product_list),
    path('product/<int:pk>/', product_detail, name='product-detail'),
    path('collection/', collection_list),
    path('collection/<int:pk>/', collection_detail, name='collection-detail')

]
