from django.contrib import admin, messages
from django.db.models import QuerySet, Count
from django.utils.html import format_html, urlencode
from django.http import HttpRequest
from django.urls import reverse
from typing import Optional
from .models import Cart, CartItem, Collection, Product, Customer, Order, OrderItem, ProductImage
from tags.models import TaggedItem
admin.site.site_header = "StoreFront"
admin.site.index_title = "Admin"

@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title','products_count']
    #return the number of products in each collection
    @admin.display(ordering='products_count')
    def products_count(self, collection):
        # reverse(admin:app_model_page)
        url = (reverse('admin:store_product_changelist') 
        + "?"
        + urlencode({
            'collection__id': str(collection.id)
        }))
        return format_html('<a href="{}">{}</a>', url, collection.products_count)

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return super().get_queryset(request).annotate(products_count=Count('product'))
class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory' # used in the query string in the search bar
    # adding fillers
    def lookups(self, request, model_admin):
        return [
            ('<10', 'Low'),
        ]
    def queryset(self, request, queryset: QuerySet) -> Optional[QuerySet]:
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)

class ProductImageInline(admin.TabularInline):
    model = ProductImage 
    readonly_fields = ['thumbnail']
    def thumbnail(self, instance):
        if instance.image.name != '':
            return format_html(f'<img src="{instance.image.url}" class="thumbnail"/>')
        return ''
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    actions = ['clear_inventory',]
    inlines = [ProductImageInline]
    search_fields = ['title',]
    list_display = ['title', 'description', 'unit_price', 'inventory_status', 'collection_title']
    list_editable = ['unit_price',]
    list_filter = ['collection','last_update', InventoryFilter]
    list_per_page = 10
    list_select_related = ['collection',]
    def collection_title(self, product):
        return product.collection.title
    @admin.display(ordering = 'inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return "LOW" 
        return "OK"
    @admin.action(description = "Clear Inventory")
    def clear_inventory(self, request, queryset):
        updatedProducts = queryset.update(inventory = 0)
        self.message_user(request, f"{updatedProducts} have been updated successfully", messages.SUCCESS)

    class  Media:
        css = {
            'all': ['store/style.css']
        }

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'membership','orders_count']
    list_editable = ['membership']
    list_per_page = 10
    list_select_related = ['user']
    ordering = ['user__first_name', 'user__last_name',]
    search_fields = ['first_name__istartswith', 'last_name__istartswith',]
    autocomplete_fields = ['user']
    # Like we did in collection we want to go to customer orders page when click on the order numbers
    @admin.display(ordering='orders_count')
    def orders_count(self, customer):
        url = (reverse('admin:store_order_changelist')
        + '?'
        + urlencode({
            'customer__id': str(customer.id)
        }))
        return format_html("<a href={}>{}</a>", url, customer.orders_count)
    
    def get_queryset(self, request : HttpRequest) -> QuerySet:
        return super().get_queryset(request).annotate( orders_count = Count('order'))

#TabularInline (table) | StackedInline (form)
class OrderItemInline(admin.TabularInline): 
    autocomplete_fields = ['product',]
    model = OrderItem
    min_num = 1
    max_num = 10 # the minimum and maxmum number of products the order should have 
    extra = 0 # the number of extra rows in the table to be displayed
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ['customer',] # for searching for a customer
    inlines = [OrderItemInline]
    list_display = ['placed_at', 'payment_status','customer']
    list_per_page = 10  
    list_select_related = ['customer']

class CartItemInline(admin.TabularInline):
    autocomplete_fields = ['product',]
    model = CartItem
    extra = 0
    min_num: 1
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    autocomplete_fields = ['customer']
    list_display =  ['id', 'created_at',]
    list_per_page = 10
    inlines = [
        CartItemInline,
    ]
    
