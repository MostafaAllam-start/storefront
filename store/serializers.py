from calendar import c
from decimal import Decimal
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from .models import Order, OrderItem, Product, Collection, ProductImage, Review, Cart, CartItem, Customer
from .signals import order_created

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']

    def create(self, validated_data):
        product_id = self.context['product_id']
        return ProductImage.objects.create(product_id=product_id, **validated_data)
class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    class Meta:
        fields = ['id', 'title', 'unit_price', 'price_with_tax','description','inventory', 'collection', 'images']
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

class OrderItemProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'unit_price']

class OrderItemSerializer(serializers.ModelSerializer):
    product = OrderItemProductSerializer()
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'unit_price', 'quantity']
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    class Meta:
        model = Order
        fields = ['id', 'customer', 'placed_at', 'payment_status', 'items']

class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['payment_status']

class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()
    def validate_cart_id(self, cart_id):
        if not Cart.objects.filter(pk=cart_id).exists():
            raise serializers.ValidationError('No cart whith the given ID was found.')
        elif CartItem.objects.filter(cart_id=cart_id).count() == 0:
            raise serializers.ValidationError('The cart is empty.') 
        return cart_id
    def save(self, **kwargs):
        with transaction.atomic():
            cart_id = self.validated_data['cart_id']
            customer = get_object_or_404(Customer, user_id=self.context['user_id'])
            order = Order.objects.create(customer=customer)
            cart_items = CartItem.objects \
                                .select_related('product') \
                                .filter(cart_id=cart_id)
            order_items = [OrderItem(
                                order=order,
                                product = item.product,
                                unit_price = item.product.unit_price,
                                quantity=item.quantity
                        )for item in cart_items
                        ]
            OrderItem.objects.bulk_create(order_items)
            Cart.objects.filter(pk=cart_id).delete()

            # Fire the order_created signal
            order_created.send_robust(self.__class__, order=order)
            return order


    