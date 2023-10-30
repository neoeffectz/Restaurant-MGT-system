from datetime import datetime
from .serializers import UserRegistrationSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import login
from .serializers import *
from rest_framework import generics
from .models import *
import json
from json import dumps
from .utils import guestOrder
from django.http import JsonResponse
from rest_framework import permissions 
from .permissions import IsManager, IsAttendant
from rest_framework.permissions import IsAuthenticated


# userregistration endpoint
class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        return Response(serializer.data)


# createproducts with permsions for manager groups
class CreateProductView(generics.ListCreateAPIView):
    queryset = MenuProducts.objects.all()
    serializer_class = MenuProductsSerializer
    permission_classes = [IsAuthenticated]

    #if user is in the manager group then it can access the post endpoint but all authenticated users can acess the get all product endpoint
    def get_permissions(self):
        if self.request.method == 'POST':
            
            self.permission_classes = [IsManager]
        
        return super(CreateProductView, self).get_permissions()
    
# delete, update, and get a single product with permsions for manager groups
class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    
    queryset = MenuProducts.objects.all()
    serializer_class = MenuProductsSerializer

    permission_classes = [IsAuthenticated]

    #if user is in the manager group then it can access the patch and delete endpoint but all authenticated users can acess the get a single product endpoint
    def get_permissions(self):
        if self.request.method == 'PATCH':
            
            self.permission_classes = [IsManager]
        
        elif self.request.method == 'DELETE':
            self.permission_classes = [IsManager]
        
        return super(ProductDetailView, self).get_permissions()
    


    

    






@api_view(['GET'])
def restaurant(request):
        
    products = MenuProducts.objects.all()

    Common_categories = Categories.objects.all()

    #getting a complete order_id
    complete_order = Order.objects.filter(complete=True)

    for order in complete_order: 
        #getting the order items with the complete order_id 
        Orderitem_list = OrderItem.objects.filter(order_id=order)

        print(Orderitem_list, "Orderitem_list LINE sth")


    
    prod_category = products.filter().values('id','name','category_id')

    


    clean_prod_category = []
    for i in prod_category:
        category_name = Categories.objects.filter(id=i['category_id']).values('name')[0]['name']
        i['category_id'] = category_name
        clean_prod_category.append(i)
    
    
    serializer = MenuProductsSerializer(products, many=True)
    serializerCategories = CategoriesSerializer(Common_categories, many=True)

    return Response(
        {
            "MenuProducts": serializer.data,  
            'restaurant_categories':serializerCategories, 
            'clean_prod_category':list(clean_prod_category),
            'title':'restaurant',
        }
    )


@api_view(["POST"])
def updateItem(request):
    serializer = UpdateItemSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    productId = int(serializer.data['productId'])
    action = serializer.data['action']
    print('action:', action)
    print('productid:', productId)
    
    
    #You need to associate a user with tokens and be able to know who did a certain action below


    # customer = request.user.customer
    # product = MenuProducts.objects.get(id=productId)

    # list_of_orders = []
    
    # order, created = Order.objects.get_or_create(customer=customer, complete=False)
    # orderItem, created = OrderItem.objects.get_or_create(order=order, product=product, productId=productId)
    
    # if action == 'add':
    #     orderItem.quantity = (orderItem.quantity + 1)
    # elif action == 'remove':
    #     orderItem.quantity = (orderItem.quantity - 1)
    
    # orderItem.save()
    # if orderItem.quantity <= 0:
    #     orderItem.delete()
    
    
    return Response(serializer.data)

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

