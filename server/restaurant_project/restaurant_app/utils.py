import json
from json import dumps
from .models import *
from django.conf import settings
from django.contrib.auth.models import User


def cookieCart(request):
	#to prevent first time loading error
	try:
		cart = json.loads(request.COOKIES['cart'])
	except:
		cart = {}
	
	
	items = []
	order = {'get_cart_total':0, 'get_cart_items':0, 'shipping': False}
	cartItems = order['get_cart_items']

	for i in cart:
		#prevent error when product added by guest is deleted from db
		try:
			cartItems += cart[i]['quantity']

			product = Products.objects.get(id=i)
			total = (product.price * cart[i]['quantity'])

			order['get_cart_total'] += total
			order['get_cart_items'] += cart[i]['quantity']

			item = {
				'product':{
					'id': product.id,
					'name': product.name,
					'price': product.price,
					'imageURL': product.imageURL,
				},
				'quantity': cart[i]['quantity'],
				'get_total': total
			}
			items.append(item)
			if product.digital == False:
				order['shipping'] = True
		except:
			pass
	return {'cartItems':cartItems, 'order':order, 'items':items}

def cartData(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		cookieData = cookieCart(request)
		cartItems = cookieData['cartItems']
		order = cookieData['order']
		items = cookieData['items']

	return {'cartItems':cartItems, 'order':order, 'items':items}


def productDet(request, products):
	all_prod = products.values()
	# print(all_prod[0])
	
	#get id and prod name
	main_array = []
	for i in range(0, len(all_prod)):
		# product package rep the product name and its id in their own array
		each_product_package = []

		# adding id to package
		prod_id = all_prod[i]["id"]
		each_product_package.append(prod_id)

		# adding name to package..
		prod_name = all_prod[i]["name"]
		each_product_package.append(prod_name)


		main_array.append(each_product_package)
	
	search_db = dumps(main_array)
	
	
	each_product_det = []
	
	for i in range(0, len(products)):
		each_product_det.append(products.values()[i])
	
	
	each_product_db = dumps(each_product_det)

	return {'each_product_db':each_product_db, 'search_db':search_db}

def guestOrder(request,data):
	name = data['shipping']['fname']
	email = data['shipping']['email']

	cookieData = cookieCart(request)
	items = cookieData['items']

	customer, created = Customer.objects.get_or_create(email=email)
	customer.name = name
	customer.save()

	order = Order.objects.create(customer=customer,complete=False)

	for item in items:
		product = MenuProducts.objects.get(id=item['product']['id'])

		orderItem = OrderItem.objects.create(
			product=product,
			order=order,
			quantity=item['quantity']
		)

	return customer, order