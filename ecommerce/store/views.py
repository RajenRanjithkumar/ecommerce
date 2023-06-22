from django.shortcuts import render
from .models import *

# Create your views here.

#https://www.youtube.com/watch?v=_ELCMngbM0E&list=PL-51WBLyFTg0omnamUjL1TCVov7yDTRng
#19:13

def store(request):

    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'store/store.html', context)

def cart(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, complete = False) # find the order if not create it
        items = order.orderitem_set.all()
    else:
        items = []
        #hard coded
        order = {'get_cart_items':0, "get_cart_total": 0}


    context = {'items': items, 'order': order}
    return render(request, 'store/cart.html', context)

def checkout(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, complete = False) # find the order if not create it
        items = order.orderitem_set.all()
    else:
        items = []
        #hard coded
        order = {'get_cart_items':0, "get_cart_total": 0}


    context = {'items': items, 'order': order}

    
    return render(request, 'store/checkout.html', context)