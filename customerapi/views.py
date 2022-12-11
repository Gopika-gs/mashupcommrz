from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from rest_framework.response import Response
from adminpannel.models import Products
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework import status
from customer.forms import RegistrationForm
from customer.models import CustomerCart
from customerapi.serializer import CustomerCartSerializer
from .serializer import ProductsListSerializer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def registercustomer(request):
    registerform = RegistrationForm(request.data)
    if registerform.is_valid():
            username = registerform.cleaned_data['username']	
            email = registerform.cleaned_data['emailid']	
            firstname = registerform.cleaned_data['firstname']	
            lastname = registerform.cleaned_data['lastname']	
            password = registerform.cleaned_data['password']	
            if  User.objects.filter(username=username).exists():
                registerform = RegistrationForm(request.POST)
                context = {'registerform':registerform.data,
                            'error':'Username already exists add a new one'}
                return Response(context,status = status.HTTP_400_BAD_REQUEST)
            else:	
                user = User.objects.create_user(username = username, 
                                                email = email, 
                                                password = password,
                                                first_name = firstname,
                                                last_name = lastname)
                user.save()
                context = {'registerform':registerform.data,'success':'Created user'}
                return Response(context,status = status.HTTP_200_OK)
    else:
        registerform = RegistrationForm(request.POST)
        context = {'registerform':registerform.data,'errors':registerform.errors}
        return Response(context,status = status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=status.HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=status.HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},status=status.HTTP_200_OK)

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def logoutcustomer(request):
    request.user.auth_token.delete()
    return Response({'message':'success'},status=status.HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def listproducts(request):
    products = Products.objects.filter(is_active=1)
    if request.user:
        context = {'userid':request.user.id}
    serializer = ProductsListSerializer(products,many=True,context=context)
    return Response(serializer.data,status=status.HTTP_200_OK)

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def productdetails(request):
    product_id = int(request.data.get("product"))
    product = Products.objects.get(id = product_id)
    if request.user:
        context = {'userid':request.user.id}
    serializer = ProductsListSerializer(product,context=context)
    return Response(serializer.data,status=status.HTTP_200_OK)



@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def addproductcart(request):
    product_id = int(request.data.get("product"))
    user = request.user
    cart_instance = CustomerCart(product_id=product_id,customer=user)
    cart_instance.save()
    return Response({'result':'success'})


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def removeproductfromcart(request):
    product_id = int(request.data.get("product"))
    user = request.user
    cart_instance = CustomerCart.objects.filter(product_id=product_id,customer=user)
    cart_instance.delete()
    return Response({'result':'success'})

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def listcustomercart(request):
    usercart = CustomerCart.objects.filter(customer = request.user).select_related('product')
    totalprice = sum(item.product.price for item in usercart)
    cartserialized = CustomerCartSerializer(usercart,many = True)
    return Response({'cartitems':cartserialized.data,'totalprice':totalprice})




