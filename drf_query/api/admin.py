from django.contrib import admin
from django.contrib.auth.models import User
from .models import Product,Order,Customer
from django.contrib.auth.admin import UserAdmin as BaseAdmin
# Register your models here.
admin.site.unregister(User)
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','unique_product_id','description','date_created','category']
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['product','customer','status','date_created']
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    pass
@admin.register(User)
class UserAdmin(BaseAdmin):
    list_display = ['id','username','email','password']
