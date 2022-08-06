from django.urls import path, include
from store.views import ProductViewSet, ReviewViewSet, CollectionViewSet
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register('product', ProductViewSet)
router.register('collection', CollectionViewSet)
#nested router to get the review of each prodcut
product_router = routers.NestedSimpleRouter(router, 'product', lookup='product')
product_router.register('reviews', ReviewViewSet,  basename='product-reviews')
urlpatterns = [
    path('', include(router.urls)), 
    path('', include(product_router.urls))
]