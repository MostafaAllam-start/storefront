from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from store.admin import ProductAdmin, ProductImageInline
from store.models import Product
from tags.models import TaggedItem
 
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    pass

class TagInline(GenericTabularInline):
    autocomplete_fields = ['tag']
    model = TaggedItem

class CustomProductAdmin(ProductAdmin):
    inlines = [TagInline, ProductImageInline]

admin.site.unregister(Product)
admin.site.register(Product, CustomProductAdmin)  
