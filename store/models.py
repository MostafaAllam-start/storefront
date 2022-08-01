from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator
class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()

class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name='+') # this + in the realated_name means don't create any realted name for this relation     

    class Meta:
        ordering = ('title',)

    def __str__(self) -> str:
        return self.title


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
    promotions = models.ManyToManyField(Promotion, null=True,blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Product, self).save(*args,*kwargs)
    
    def __str__(self) -> str:
        return self.title

class Customer(models.Model):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'
    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD, 'Gold'),
    ]
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=12)
    birth_date = models.DateField(null=True, blank=True)
    membership = models.CharField(choices=MEMBERSHIP_CHOICES, max_length=1, default=MEMBERSHIP_BRONZE)

    def __str__(self) -> str:
        return self.first_name+" "+self.last_name

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
    PAYMENT_STATUS_FAILD = 'F'
    PAYMENT_STATUS = [
        (PAYMENT_STATUS_PENDING , 'pending'),
        (PAYMENT_STATUS_COMPLETED, 'completed'),
        (PAYMENT_STATUS_FAILD, 'faild'),
    ]
    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=1, choices=PAYMENT_STATUS, default=PAYMENT_STATUS_PENDING)
    customer = models.ForeignKey(
        Customer, on_delete=models.PROTECT
    )
    class Meta:
        ordering = ('placed_at',)
    def __str__(self):
        return f"Order: {self.pk} "
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6,decimal_places=2)

class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ('created_at',)

class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()
    
