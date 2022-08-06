from rest_framework import serializers
from decimal import Decimal
from store.models import Product, Collection, Review

class ProductSerializer(serializers.ModelSerializer):
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')

    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)
    class Meta:
        fields = ['id', 'title', 'unit_price', 'price_with_tax','description','inventory', 'collection']
        model = Product
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'name', 'description', 'date']
        model = Review
    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)
class CollectionSerializer(serializers.ModelSerializer):
    products_count = serializers.SerializerMethodField(method_name='calculate_products')
    def calculate_products(self, collection: Collection):
        return collection.product_set.count()
    class Meta:
        fields = ['id','title','products_count']
        model = Collection

