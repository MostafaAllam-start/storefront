from .models import OrderItem, Product, Collection, Review 
from .serializers import CollectionSerializer, ProductSerializer, ReviewSerializer
from rest_framework.response import Response 
from rest_framework import status
from rest_framework import viewsets

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

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



    

