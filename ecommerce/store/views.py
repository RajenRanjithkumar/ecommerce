from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json
import datetime

# Create your views here.

#https://www.youtube.com/watch?v=woORrr3QNh8&list=RDCMUCTZRcDjjkVajGL6wd76UnGg&index=4
#1:19:02

def store(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, complete = False) # find the order if not create it
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items


    else:
        items = []
        #hard coded
        order = {'get_cart_items':0, "get_cart_total": 0, "shipping": False}
        cartItems = order['get_cart_items']




    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)

def cart(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, complete = False) # find the order if not create it
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        #hard coded
        order = {'get_cart_items':0, "get_cart_total": 0 , "shipping": False}
        cartItems = order['get_cart_items']


    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)

def checkout(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, complete = False) # find the order if not create it
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        
    else:
        items = []
        #hard coded
        order = {'get_cart_items':0, "get_cart_total": 0}
        cartItems = order['get_cart_items']


    context = {'items': items, 'order': order, 'cartItems': cartItems , "shipping": False}

    
    return render(request, 'store/checkout.html', context)



def updateItem(request):

    data = json.loads(request.body)
    productId = data['productID']
    action = data['action']

    print("Action", action)
    print("ProductId", productId)

    customer = request.user.customer
    product = Product.objects.get( id = productId)

    # query to the specific order
    order, created = Order.objects.get_or_create(customer = customer, complete = False) 

    orderItem, created = OrderItem.objects.get_or_create(order = order, product = product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity) + 1
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity) - 1

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

def processOrder(request):

    # user data from front end
    # print('Data:', request.body)

    data = json.loads(request.body)

    trasaction_id = datetime.datetime.now().timestamp()

    if request.user.is_authenticated:
        customer = request.user.customer
         # query to the specific order
        order, created = Order.objects.get_or_create(customer = customer, complete = False) 
        total = float(data['form']['total'])
        order.trasacrion_id = trasaction_id

        # to cross check the total cost
        if total == order.get_cart_total:
            order.complete = True

        order.save()

        if order.shipping == True:
            ShippingAddress.objects.create(

                customer = customer,
                order = order,
                address = data['shipping']['address'],
                city = data['shipping']['city'],
                state = data['shipping']['state'],
                zipcode = data['shipping']['zipcode'],


            )
        # else handle for the digital products


    else:
        print("User not logged in")




    # print('Data:', request.body)

    return JsonResponse("Payment complete", safe=False)
