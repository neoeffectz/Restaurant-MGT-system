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
import json
from json import dumps
from .utils import guestOrder, cartData, productDet


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # added token creation in the endpoint so token can be generated on sign up
        token, created = Token.objects.get_or_create(user=user)

        return Response({"detail": "User registered successfully.", "token": token.key}, status=201)


class UserAuthenticationView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = UserAuthenticationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        login(request, user)

        token, created = Token.objects.get_or_create(user=user)

        
        return Response({"detail": "User logged in successfully.",  "token": token.key})


def restaurant(request):
    data = cartData(request)
    cartItems = data['cartItems']
        
    products = MenuProducts.objects.all()
    product_db = productDet(request,products)

    #getting a complete order_id
    complete_order = Order.objects.filter(complete=True)

    for order in complete_order: 
        #getting the order items with the complete order_id 
        Orderitem_list = OrderItem.objects.filter(order_id=order)

        print(Orderitem_list, "Orderitem_list LINE 92")
        # print(Products.objects.filter(name=Orderitem_list[0])[0].id)
        print(order, "Orderitem_list LINE 65")


    Common_categories = Categories.objects.all()
    prod_category = products.filter().values('id','name','category_id')

    restaurant_categories_id = products.filter().values('category_id')
    restaurant_categories = []
    for s_cat in restaurant_categories_id:
        restaurant_categories_name = Categories.objects.get(id=s_cat['category_id'])
        restaurant_categories.append(restaurant_categories_name.name)


    clean_prod_category = []
    for i in prod_category:
        category_name = Categories.objects.filter(id=i['category_id']).values('name')[0]['name']
        i['category_id'] = category_name
        clean_prod_category.append(i)
    
    context = {
        'products':products,
        'restaurant_categories':list(set(restaurant_categories)),
        'clean_prod_category':dumps(clean_prod_category),
        "each_product_db":product_db['each_product_db'],
        'search_db':product_db['search_db'], 
        'cartItems':cartItems,
        'title':'restaurant',
        'Common_categories':Common_categories,
        }
    return render(request, 'restaurant/restaurant.html', context)





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

