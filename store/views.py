from django.shortcuts import get_object_or_404
from .models import Product, Collection 
from .serializers import CollectionSerializer, ProductSerializer
from rest_framework.response import Response 
from rest_framework.decorators import api_view
from rest_framework import status

@api_view(['Get', 'POST'])
def product_list(request):
    if request.method == 'GET':
        queryset = Product.objects.prefetch_related('promotions').select_related('collection')
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.validated_data,status=status.HTTP_201_CREATED)



@api_view(['GET','PUT','DELETE'])
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=id)
    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return  Response(serializer.data)
    elif request.method == 'DELETE':
        if product.orderitem_set.count() > 0:
            return Response({"error": "Product cannot be deleted"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)    

@api_view(['GET', 'POST'])
def collection_list(request):
    if request.method == 'GET':
        queryset = Collection.objects.prefetch_related('product_set').all()
        print(queryset)
        serializer = CollectionSerializer(queryset, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CollectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status= status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
def collection_detail(request, pk):
    collection = get_object_or_404(Collection, pk=pk)
    if request.method == 'GET':
        serializer = CollectionSerializer(collection)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = CollectionSerializer(collection, data= request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        if collection.product_set.count() > 0:
            return Response({'error':'Collection cannot be deleted.'}, status=status.HTTP_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)