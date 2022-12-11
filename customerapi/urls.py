from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('registercustomer', views.registercustomer, name='registercustomerapi'),
    path('logincustomer', views.login, name='logincustomerapi'),
    path('logoutcustomer', views.logoutcustomer, name='logoutcustomerapi'),
    path('listproducts', views.listproducts, name='listproductsapi'),
    path('productdetails', views.productdetails, name='productdetailsapi'),
    path('addproductcart', views.addproductcart, name='addproductcartapi'),
    path('removeproductfromcart', views.removeproductfromcart, name='removeproductfromcartapi'),
    path('listcustomercart', views.listcustomercart, name='listcustomercartapi'),
     ]