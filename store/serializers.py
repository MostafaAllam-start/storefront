from rest_framework import serializers
from decimal import Decimal
from .models import Product, Collection, Review, Cart, CartItem, Customer
class ProductSerializer(serializers.ModelSerializer):
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    class Meta:
        fields = ['id', 'title', 'unit_price', 'price_with_tax','description','inventory', 'collection']
        model = Product

    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'name', 'description', 'date']
        model = Review
    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)
class CollectionSerializer(serializers.ModelSerializer):
    products_count = serializers.SerializerMethodField(method_name='calculate_products')
    class Meta:
        fields = ['id','title','products_count']
        model = Collection
    def calculate_products(self, collection: Collection):
        return collection.product_set.count()
# if we want to show only some filds of the product serializer we have to define another serialzer
class CartItemProductSerializer(serializers.ModelSerializer):
        class Meta:
            fields = ['id', 'title', 'unit_price']
            model = Product

class CartItemSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField(method_name='calculate_total_price')
    product = CartItemProductSerializer()
    class Meta:
        fields = ['id', 'product', 'quantity','total_price']
        model = CartItem

    def calculate_total_price(self, cart_item:CartItem):
        price = cart_item.product.unit_price * cart_item.quantity
        return price

    def create(self, validated_data):
        cart_id = self.context['cart_id']
        return CartItem.objects.create(cart_id=cart_id, **validated_data)

class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(read_only=True, many=True)
    total_price = serializers.SerializerMethodField(method_name='calculate_total_price')
    class Meta:
        fields = ['id', 'created_at', 'customer', 'items', 'total_price']
        model = Cart

    def calculate_total_price(self, cart: Cart):
        # price = 0
        # for item in cart.items.all():
        #     price += item.product.unit_price * item.quantity
        return sum([item.product.unit_price * item.quantity for item in cart.items.all()])

class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()
    class Meta:
        fields = ['id', 'product_id', 'quantity']
        model = CartItem 

    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError('No product with the given id was found')
        return value
    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']
        #saving logic
        try:
            # updating e-xisting item 
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            # creating a brand new item
            self.instance = CartItem.objects.create(cart_id=cart_id, **self.validated_data)
        return self.instance # just to follow up the implementation of the save method in the ModelSerializer base class

class UpdateCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField
    class Meta:
        fields = ['quantity']
        model = CartItem

class CustomerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only= True)
    class Meta:
        model = Customer
        fields = ['id', 'user_id', 'phone', 'birth_date', 'membership',]

