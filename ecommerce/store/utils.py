import json
from .models import *


def cookieCart(request):

    # for guest users get the cart values from the cookies
    #handle if the guest cart is empty
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {} 

    print('cart:', cart)
    items = []
    #hard coded
    order = {'get_cart_items':0, "get_cart_total": 0 , "shipping": False}
    cartItems = order['get_cart_items']
    
    for i in cart:
        # try block to handle if the cookie has a product that have been removed from the db
        try:
            cartItems += cart[i]['quantity']

            product = Product.objects.get(id = i)

            total = (product.price * cart[i]['quantity'])

            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']

            item = {
                'product':{

                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'imageURL': product.imageURL
                },
                'quantity': cart[i]['quantity'],
                'get_total': total
            }

            items.append(item)

            if product.digital == False:
                order['shipping'] = True
        except:
            pass

    return {'items': items, 'order': order, 'cartItems': cartItems}


def cartData(request):


    if request.user.is_authenticated:
        # get the data from backend db
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, complete = False) # find the order if not create it
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        
    else:
        # get the data from front end cookies "cart"
        # items = []
        # #hard coded
        # order = {'get_cart_items':0, "get_cart_total": 0}
        # cartItems = order['get_cart_items']

        cookieData = cookieCart(request)
        order = cookieData['order']
        items = cookieData['items']
        cartItems = cookieData['cartItems']

    return {'items': items, 'order': order, 'cartItems': cartItems}