from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Product,Order

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','name','unique_product_id','description','date_created','category']
        
    def validate(self, data):
        if Product.objects.filter(name=data['name']).exists():
            raise serializers.ValidationError("Product Name already exists")
        elif Product.objects.filter(unique_product_id=data['unique_product_id']).exists():
            raise serializers.ValidationError("Unique ID already exists")
        return data
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id','product','customer','date_created','status']
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email','password']