from dataclasses import fields
from adminpannel.models import Products
from customer.forms import LoginForm, RegistrationForm
from customer.models import CustomerCart
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token['username'] = user.username
        return token
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','email','password','first_name','last_name')

        def logincustomer(request):
            username = request.data.get("username")#geting the data from the request
            password = request.data.get("password")

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','first_name','last_name', 'email','password')
        extra_kwargs = {'password': {'write_only': True}}

    def registercustomer(self,request):
        registerform = RegistrationForm(request.data)
        if registerform.is_valid():
            user = User.objects.create_user(
                    self.cleaned_data['username'],
                    self.cleaned_data['first_name'],
                    self.cleaned_data['last_name'],
                    self.cleaned_data['email'],
                    self.cleaned_data['password'])

        return user




class ProductsListSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Products
        fields = '__all__'


    def to_representation(self, obj):
        serialized_data = super(ProductsListSerializer, self).to_representation(obj)
        product_id = serialized_data.get('id')
        if self.context.get("userid"):
            try:
                customercart = CustomerCart.objects.get(product_id=product_id,customer_id=self.context.get("userid"))
                serialized_data['incart'] = 1
            except:
                serialized_data['incart'] = 0
        else:
            serialized_data['incart'] = 0
        return serialized_data

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ('__all__')


class CustomerCartSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    class Meta:
        model = CustomerCart
        fields = ('__all__')