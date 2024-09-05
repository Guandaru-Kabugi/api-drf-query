from django.test import TestCase,SimpleTestCase,Client
from .models import Product,Order,Customer
from django.contrib.auth.models import User
from django.urls import reverse,resolve
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase
from rest_framework.test import force_authenticate
from .views import SpecificUserOrderFilter,OrderViewFilter,OrderListView,ProductListView,OrderCreateDeleteView,ProductCreateView,signup,login
# Create your tests here.
#we start with testing urls
#research how to test urls involving include and router
"""class TestUrls(SimpleTestCase):
    def test_login_url_is_resolved(self):
        url = reverse('login')
        # print(resolve(url))
        self.assertEqual(resolve(url).func,login)
    def test_signup_url_is_resolved(self):
        url = reverse('signup')
        # print(resolve(url))
        self.assertEqual(resolve(url).func,signup)
    def test_productview_url_is_resolved(self):
        url = reverse('productview')
        # print(resolve(url))
        self.assertEqual(resolve(url).func.view_class,ProductCreateView)
    def test_productlist_url_is_resolved(self):
        url = reverse('productlist')
        # print(resolve(url))
        self.assertEqual(resolve(url).func.view_class,ProductListView)
    def test_orderlist_url_is_resolved(self):
        url = reverse('orderlist')
        # print(resolve(url))
        self.assertEqual(resolve(url).func.view_class,OrderListView)    
    def test_clientlist_url_is_resolved(self):
        url = reverse('clientlist',kwargs={'username': 'testuser'})
        # print(resolve(url))
        self.assertEqual(resolve(url).func.view_class,OrderViewFilter)   
    def test_specificlist_url_is_resolved(self):
        url = reverse('specificlist')
        # print(resolve(url))
        self.assertEqual(resolve(url).func.view_class,SpecificUserOrderFilter) 
    def test_ordercreateview_url_is_resolved(self):
        url = reverse('ordercreatedeleteview-list')
        # print(resolve(url))
        self.assertEqual(resolve(url).func.cls,OrderCreateDeleteView)  
    # def test_createview_url_is_resolved(self):
    #     url = reverse('ordercreatedeleteview-list')
    #     print(resolve(url)) """
#Testing views -------
"""class TestView(TestCase):
    def setUp(self):
        self.client = Client()
        self.list_url = reverse('productlist')
        self.order_list = reverse('orderlist')
        self.orderview_filter = reverse('clientlist',kwargs={'username': 'testuser'})
        self.specificorder = reverse('specificlist')
        self.productcreateview = reverse('productview')
        self.clientlogin = reverse('login')
        self.signupview = reverse('signup')
        self.ordercreatedelete = reverse('ordercreatedeleteview-list')
        self.product = Product.objects.create(
            name='Cookies',
            description='sweet cookies',
            unique_product_id='001',
            date_created='2024-11-11',
            category='bakery'
        )
        self.new_user = User.objects.create_user(username='test_user',email='testuser@gmail.com',password='testuser1234.')
        self.client.force_login(user=self.new_user)
    def test_product_list_GET(self):
        
        
        response = self.client.get(self.list_url)
        
        self.assertEquals(response.status_code,200)
    def test_order_view_GET(self):
        
        response = self.client.get(self.order_list)
        
        self.assertEquals(response.status_code,200)
    def test_order_view_filter_GET(self):
        
        response = self.client.get(self.orderview_filter)
        
        self.assertEquals(response.status_code,200)
    def test_specific_order_filter_GET(self):
        
        response = self.client.get(self.specificorder)
        
        self.assertEquals(response.status_code,200)
    def test_product_create_view_POST(self):
        
        self.order = Order.objects.create(
            product=self.product,
            customer=self.new_user,  # You should pass the User, not the client
            date_created='2024-08-08',
            status='pending')
        
        response = self.client.post(self.ordercreatedelete, {
        'product': self.product.id,
        'customer': self.new_user.id,
        'date_created': '2024-08-08',
        'status': 'pending'
    })
        
        self.assertEquals(response.status_code,201)
        self.assertEquals(self.order.product.name, 'Cookies')
    def test_order_list_view_GET(self):
        
        response = self.client.get(self.ordercreatedelete)
        
        self.assertEquals(response.status_code,200)
    def test_login_view_POST(self):
        
        response = self.client.post(self.clientlogin,{
            'username':'test_user',
            'password':'testuser1234.'
        })
        self.assertEquals(response.status_code,200)
    def test_signup_view_POST(self):
        
        response = self.client.post(self.signupview,{
            'username':'Alex',
            'password':'Alex1234.',
            'email':'alex1234@gmail.com'
        })
        
        self.assertEquals(response.status_code,200)"""
# testing models...............
"""class TestModels(TestCase):
    def setUp(self):
        self.product1 = Product.objects.create(
            name='Cookies',
            description='sweet cookies',
            unique_product_id='001',
            date_created='2024-11-11',
            category='bakery'
        )
        self.client = Client()
        self.new_user = User.objects.create_user(username='test_user',email='testuser@gmail.com',password='testuser1234.')
    def test_product_has_been_created(self):
        self.assertEquals(self.product1.name,'Cookies')
    def test_order_has_been_created(self):
        self.order = Order.objects.create(
            product=self.product1,
            customer=self.new_user,  # You should pass the User, not the client
            date_created='2024-08-08',
            status='pending'
        )
        self.assertEquals(self.order.customer.id, self.new_user.id)"""


#using api requestfactory
factory = APIRequestFactory()
request = factory.get('productlistview/')
class TestProductView(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.productview_url = reverse('productlist')
        self.new_user = User.objects.create_user(username='James',password='James1234',email='james@gmail.com')
        self.user = User.objects.get(username='James')
    def test_product_list_view(self):
        request = self.factory.get(self.productview_url)
        force_authenticate(request, user=self.user)
        response = ProductListView.as_view()(request)
        
        self.assertEquals(response.status_code,200)