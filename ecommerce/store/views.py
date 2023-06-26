from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json

# Create your views here.

#https://www.youtube.com/watch?v=woORrr3QNh8&list=RDCMUCTZRcDjjkVajGL6wd76UnGg&index=3
#26:45

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