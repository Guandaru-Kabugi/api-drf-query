from django.urls import path,include,re_path
from .views import login,signup,ProductCreateView,OrderCreateDeleteView,ProductListView,OrderListView,SpecificUserOrderFilter,OrderViewFilter
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'orders',OrderCreateDeleteView,basename='ordercreatedeleteview')
urlpatterns = [
    path('',include(router.urls)),
    path('api-auth/',include('rest_framework.urls')),
    path('login/',login,name='login'),
    path('signup/',signup,name='signup'),
    path('productcreateview/',ProductCreateView.as_view(),name='productview'),
    path('productlistview/',ProductListView.as_view(),name='productlist'),
    path('orderlistview/',OrderListView.as_view(),name='orderlist'),
    re_path('^clientorders/(?P<username>.+)/$',OrderViewFilter.as_view(),name='clientlist'),
    path('specificuserorderfilter/',SpecificUserOrderFilter.as_view(),name='specificlist'),
]
