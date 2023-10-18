from django.shortcuts import render
from rest_framework.response import Response
from .serializers import UserRegistrationSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import login
from .serializers import UserAuthenticationSerializer
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics


from .models import *
from django.http import HttpResponseRedirect, JsonResponse
import json
from json import dumps
import datetime
from django.contrib.auth.decorators import login_required
from .utils import guestOrder


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({"detail": "User registered successfully."}, status=201)


class UserAuthenticationView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = UserAuthenticationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        login(request, user)

        
        token, created = Token.objects.get_or_create(user=user)

        return Response({"detail": "User logged in successfully.", "token": token.key})



def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('action:', action)
    print('product:', productId)
    
    
    customer = request.user.customer
    product = MenuProducts.objects.get(id=productId)

    list_of_orders = []
    
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product, productId=productId)
    
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    
    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()
    
    
    return JsonResponse('item added', safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        
        # for orders in Order.objects.filter().values():
        #     if len(str(orders['transaction_id'])) < 4:
        #         print(str(orders['transaction_id']))
        #         Order.objects.get(id=orders['id']).delete()
        
        

    else:
        customer, order = guestOrder(request,data)
        

    total = float(data['shipping']['total'])
    order.transaction_id = transaction_id
    
    if total == float(order.get_cart_total):
        order.complete = False
        order.pending = True
        order.cancelled = False
    order.save()

    # ShippingModel.objects.create(
    #     customer=customer,
    #     order=order,
    #     #more fields according to model
    
    # )


    return JsonResponse('payment complete', safe=False)

