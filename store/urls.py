from django.urls import path
from .views import ProductViewSet, CollectionViewSet
from rest_framework.routers import SimpleRouter
router = SimpleRouter()
router.register('product', ProductViewSet)
router.register('collection', CollectionViewSet)
urlpatterns = router.urls