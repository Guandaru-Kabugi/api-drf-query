from django.shortcuts import render,get_object_or_404
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.decorators import permission_classes,api_view
from .models import Product,Order
from .serializers import OrderSerializer,ProductSerializer,UserSerializer
from rest_framework.generics import ListAPIView,CreateAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.http import HttpResponse
# Create your views here.
@api_view(['POST'])
def login(request):
    user = get_object_or_404(User,username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response({"Details":"Not Found"},status=status.HTTP_400_BAD_REQUEST)
    token,created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)
    return Response({"token":token.key, "user":serializer.data})
@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user=user)
    return Response({"token":token.key,"user":serializer.data})
@permission_classes([IsAuthenticated,IsAdminUser])
class ProductCreateView(CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
@permission_classes([IsAuthenticated])
class OrderCreateDeleteView(ModelViewSet):
    # queryset = Order.objects.all()
    serializer_class = OrderSerializer
    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(customer=user)
    
    def perform_create(self, serializer):
        # Example: Automatically assign the customer as the logged-in user
        serializer.save(customer=self.request.user)
@permission_classes([IsAuthenticated])
class ProductListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
@permission_classes([IsAuthenticated])
class OrderListView(ListAPIView):
    serializer_class = OrderSerializer
    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(customer=user)
    
@permission_classes([IsAuthenticated])
class OrderViewFilter(ListAPIView):
    serializer_class = OrderSerializer
    def get_queryset(self):
        username = self.kwargs['username']
        return Order.objects.filter(customer__username=username)

class SpecificUserOrderFilter(ListAPIView):
    serializer_class = OrderSerializer
    #http://127.0.0.1:8000/specificuserorderfilter/?username=Manny
    def get_queryset(self):
        queryset = Order.objects.all()
        username = self.request.query_params.get('username')
        if username is not None:
            queryset = queryset.filter(customer__username=username)
        elif username is None:
            return HttpResponse('You must be registered first')
        return queryset
    
#using filterbackends
"""
from rest_framework import filters

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'email']
    
http://example.com/api/users?search=russell
"""