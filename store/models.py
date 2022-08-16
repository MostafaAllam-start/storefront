from django.db import models
from django.conf import settings
from django.contrib import admin
from django.core.validators import MinValueValidator
from uuid import uuid4
class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()

class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name='+') # this + in the realated_name means don't create any realted name for this relation     

    def __str__(self) -> str:
        return self.title
    class Meta:
        ordering = ('id',)



class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField() 
    unit_price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(1)])
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(
        Collection, on_delete=models.SET_NULL, null='True')
    promotions = models.ManyToManyField(Promotion,blank=True)

    def __str__(self) -> str:
        return self.title
class Review(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)



class Customer(models.Model):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'
    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD, 'Gold'),
    ]
    phone = models.CharField(max_length=12)
    birth_date = models.DateField(null=True, blank=True)
    membership = models.CharField(choices=MEMBERSHIP_CHOICES, max_length=1, default=MEMBERSHIP_BRONZE)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self) -> str:
        if self.user.first_name and self.user.last_name:
            return self.user.first_name+" "+self.user.last_name
        return self.user.username
    
    @admin.display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name

    @admin.display(ordering='user__last_name')
    def last_name(self):
        return self.user.last_name
    
    def email(self):
        return self.user.email
    
    class Meta:
        ordering = ['user__first_name', 'user__last_name']
        permissions = [
            ('view_history', 'Can view history')
        ]

class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zip = models.CharField(max_length=255)
    #customer = models.OneToOneField(Customer, on_delete=models.CASCADE, primary_key=True)
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE
    )

    
class Order(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETED = 'C'
    PAYMENT_STATUS_FAILED = 'F'
    PAYMENT_STATUS = [
        (PAYMENT_STATUS_PENDING , 'pending'),
        (PAYMENT_STATUS_COMPLETED, 'completed'),
        (PAYMENT_STATUS_FAILED, 'faild'),
    ]
    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=1, choices=PAYMENT_STATUS, default=PAYMENT_STATUS_PENDING)
    customer = models.ForeignKey(
        Customer, on_delete=models.PROTECT
    )
    def __str__(self):
        return f"Order: {self.pk} "
    
    class Meta:
        ordering = ('placed_at',)
        permissions = [
            ('cancel_order', 'Can cancel Order')                
        ]
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6,decimal_places=2)

class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.customer} Cart'
    class Meta:
        ordering = ('created_at',)

class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart, 
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE
    )
    quantity = models.PositiveSmallIntegerField(
        validators = [MinValueValidator(1)]
    )

    def __str__(self):
        return f'{self.product}'
    class Meta:
        unique_together = [['cart', 'product']] # For each cart the product should be unique
    
    
