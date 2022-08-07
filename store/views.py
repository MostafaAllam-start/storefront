from rest_framework import status, viewsets, mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response 
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .paginations import DefaultPagination
from .serializers import AddCartItemSerializer, CartItemSerializer, CartSerializer, CollectionSerializer, ProductSerializer, ReviewSerializer, UpdateCartItemSerializer
from .models import Cart, CartItem, OrderItem, Product, Collection, Review 
from .filters import ProductFilter

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    pagination_class = DefaultPagination
    search_fields = ['title', 'description']
    ordering_fields = ['unit_price']
    
    def get_serializer_conntext(self):
        return{'request', self.request}
    
    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id= kwargs['pk']).count() > 0:
            return Response({'error':'This Product cannot be deleted as it has been ordered'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])

    def get_serializer_context(self):
        return {'product_id':self.kwargs['product_pk']}

class CollectionViewSet(viewsets.ModelViewSet):
    queryset = Collection.objects.prefetch_related('product_set').all()        
    serializer_class = CollectionSerializer
    def destroy (self, request, *args, **kwargs):
        if Product.objects.filter(collection_id=kwargs['pk']).count() > 0:
            return Response({'error':'This Collection cannot be deleted as it has some associated prodcuts'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)

class CartViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  GenericViewSet):
    queryset = Cart.objects.prefetch_related('items__product').all() #egr load the items with their related products
    serializer_class = CartSerializer

class CartItemViewSet(viewsets.ModelViewSet):
    # preventing the PUT requests
    http_method_names = ['get', 'post', 'patch', 'delete']
    def get_serializer_class(self):
        if  self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer
    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}
    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs['cart_pk']).select_related('product')
    def retrieve(self, request, pk=None, cart_pk=None):
        cart_item = get_object_or_404(self.get_queryset(),id=pk)
        cart_item_seralizer = CartItemSerializer(cart_item)
        return Response(cart_item_seralizer.data)



    

