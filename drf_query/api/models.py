from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Product(models.Model):
    CATEGORIES =[
        ('groceries','Groceries'),
        ('grains','Grains'),
        ('bakery', 'Bakery'),
        ('clothes','Clothes'),
        ('shoes', 'Shoes'),
        ('electronics','electronics'),
        ('cooking oil', 'Cooking Oil'),
        ('flour','Flour'),
    ]
    name = models.CharField(max_length=100,null=False,verbose_name='Product Name')
    unique_product_id = models.CharField(max_length=10,unique=True,null=False, verbose_name='unique product id')
    description = models.CharField(max_length=200,null=False,verbose_name='Product Description')
    date_created = models.DateField(auto_now_add=True)
    category = models.CharField(max_length=100,choices=CATEGORIES,null=False)
    def __str__(self):
        return f"{self.name} {self.unique_product_id}"
class Customer(User):
    class Meta:
        proxy = True
    def __str__(self):
        return self.username
    @property
    def orders(self):
        order_count = self.order_set_all().count()
        return str(order_count)
class Order(models.Model):
    STATUS = [
        ('pending','Pending'),
        ('Out for delivery','Out for delivery'),
        ('Delivered', 'Delivered'),
    ]
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    date_created = models.DateField(auto_now_add=True)
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True)
    status = models.CharField(max_length=100,choices=STATUS,null=True)
