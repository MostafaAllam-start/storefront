from django.urls import path, re_path,include
from store.views import CartItemViewSet, CartViewSet, CustomerViewSet, OrderViewSet, ProductViewSet, ReviewViewSet, CollectionViewSet
from rest_framework_nested import routers
router = routers.DefaultRouter()
router.register('products', ProductViewSet, basename='products')
router.register('collections', CollectionViewSet)
router.register('cart', CartViewSet)
router.register('customer', CustomerViewSet)
router.register('orders', OrderViewSet, basename='orders')
#nested router to get the review of each prodcut
product_router = routers.NestedSimpleRouter(router, 'products', lookup='product')
product_router.register('reviews', ReviewViewSet,  basename='product-reviews')
#nested router to get the items of each cart
cart_router = routers.NestedSimpleRouter(router, 'cart', lookup='cart')
cart_router.register('items', CartItemViewSet, basename='cart-items')
urlpatterns = [
    path('', include(router.urls)), 
    path('', include(product_router.urls)),
    path('', include(cart_router.urls)),
    re_path(r'^auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.jwt')),
]