from django.urls import path, include
from store.views import ProductViewSet, ReviewViewSet, CollectionViewSet
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register('products', ProductViewSet, basename='products')
router.register('collections', CollectionViewSet)
#nested router to get the review of each prodcut
product_router = routers.NestedSimpleRouter(router, 'products', lookup='product')
product_router.register('reviews', ReviewViewSet,  basename='product-reviews')
urlpatterns = [
    path('', include(router.urls)), 
    path('', include(product_router.urls))
]