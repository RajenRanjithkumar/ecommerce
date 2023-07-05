from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages  
from django.http import JsonResponse
import json
import datetime
from .utils import cookieCart, cartData, guestOrder
from .forms import CreateCustomerForm

from django.contrib.auth.forms import UserCreationForm  #djangos default form
from django.contrib.auth import authenticate, login, logout


# Create your views here.

#https://www.youtube.com/watch?v=kH2FOWuA4uI&list=PL-51WBLyFTg0omnamUjL1TCVov7yDTRng&index=6
#49:48






def store(request):

    data = cartData(request)
    order = data['order']
    items = data['items']
    cartItems = data['cartItems']

    #moved to ulits.py
    # if request.user.is_authenticated:
    #     customer = request.user.customer
    #     order, created = Order.objects.get_or_create(customer = customer, complete = False) # find the order if not create it
    #     items = order.orderitem_set.all()
    #     cartItems = order.get_cart_items


    # else:
    #     #hard coded
    #     # items = []
        
    #     # order = {'get_cart_items':0, "get_cart_total": 0, "shipping": False}



    #     # cartItems = order['get_cart_items']

    #     cookieData = cookieCart(request)
    #     #order = cookieData['order']
    #     #items = cookieData['items']
    #     cartItems = cookieData['cartItems']



    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)


def loginUser(request):


    data = cartData(request)
    order = data['order']
    items = data['items']
    cartItems = data['cartItems']
            


    page = "login"

    username = request.POST.get('username')
    password = request.POST.get('password')

    

    if username != '' and password != '':
        try:
            user = User.objects.get(username = username)
            customer = Customer(user=user)
            customer.save()
        except:

            messages.error(request, " User does not exist ") #Django flash messages
    else:
        messages.error(request, " Username or password cannot be empty ") #Django flash messages

    

    customer = authenticate(request, username=username, password=password)

    if customer is not None:
        login(request, user)
        return redirect('store')
    
    else:
        messages.error(request, "Username or password does not exist")



    context = {"page": page, 'cartItems': cartItems}
    return render(request, 'store/login.html', context) 

def registerUser(request):

    form = CreateCustomerForm()
    

    if request.method == 'POST':
        form = CreateCustomerForm(request.POST)
        if form.is_valid():
            
            user = form.save(commit=False)

            
            user.username = user.username.lower()
            user.save()

            # #login(request, user)

            Customer.objects.create(

                user = user,
                name = user.username,
                email = user.email

            )
            return redirect('login')
        else:

            messages.error(request, "An error occured during registration")

    context = {'form': form}
    return render(request, 'store/login.html', context) 




def cart(request):

    data = cartData(request)
    order = data['order']
    items = data['items']
    cartItems = data['cartItems']

    #Logic moved to ulits.py 2
    # if request.user.is_authenticated:
    #     customer = request.user.customer
    #     order, created = Order.objects.get_or_create(customer = customer, complete = False) # find the order if not create it
    #     items = order.orderitem_set.all()
    #     cartItems = order.get_cart_items
    # else:

    #     cookieData = cookieCart(request)
    #     order = cookieData['order']
    #     items = cookieData['items']
    #     cartItems = cookieData['cartItems']

        # Logic moved to ulits.py 1
        
        # for guest users get the cart values from the cookies
        #handle if the guest cart is empty
        
        # try:
        #     cart = json.loads(request.COOKIES['cart'])
        # except:
        #     cart = {} 


        # print('cart:', cart)
        # items = []
        # #hard coded
        # order = {'get_cart_items':0, "get_cart_total": 0 , "shipping": False}
        # cartItems = order['get_cart_items']
        
        # for i in cart:
        #     # try block to handle if the cookie has a product that have been removed from the db
        #     try:
        #         cartItems += cart[i]['quantity']

        #         product = Product.objects.get(id = i)

        #         total = (product.price * cart[i]['quantity'])

        #         order['get_cart_total'] += total
        #         order['get_cart_items'] += cart[i]['quantity']

        #         item = {
        #             'product':{

        #                 'id': product.id,
        #                 'name': product.name,
        #                 'price': product.price,
        #                 'imageURL': product.imageURL
        #             },
        #             'quantity': cart[i]['quantity'],
        #             'get_total': total
        #         }

        #         items.append(item)

        #         if product.digital == False:
        #             order['shipping'] = True
        #     except:
        #         pass
            

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)

def checkout(request):

    data = cartData(request)
    order = data['order']
    items = data['items']
    cartItems = data['cartItems']

    #logic moved to utils.py
    # if request.user.is_authenticated:
    #     customer = request.user.customer
    #     order, created = Order.objects.get_or_create(customer = customer, complete = False) # find the order if not create it
    #     items = order.orderitem_set.all()
    #     cartItems = order.get_cart_items
        
    # else:
    #     # items = []
    #     # #hard coded
    #     # order = {'get_cart_items':0, "get_cart_total": 0}
    #     # cartItems = order['get_cart_items']

    #     cookieData = cookieCart(request)
    #     order = cookieData['order']
    #     items = cookieData['items']
    #     cartItems = cookieData['cartItems']


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

    if orderItem.quantity <= 0 or action =='delete':
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
        

        
        # else handle for the digital products


    else:
        # porcess guest user oders
        print("User not logged in")

        customer, order = guestOrder(request, data)

        #moved to util.py 3
        

    total = float(data['form']['total'])
    order.trasacrion_id = trasaction_id

    # to cross check the total cost

    print(round(total))
    print(round(order.get_cart_total))
    if round(total) == round(order.get_cart_total):
        order.complete = True

    print(order.trasacrion_id)
    print(order.customer)
    print(order.complete)
    

    
     


    if order.shipping == True:
            ShippingAddress.objects.create(

                customer = customer,
                order = order,
                address = data['shipping']['address'],
                city = data['shipping']['city'],
                state = data['shipping']['state'],
                zipcode = data['shipping']['zipcode'],


            )




    # print('Data:', request.body)
    order.save()

    return JsonResponse("Payment complete", safe=False)


def logoutUser(request):
    
    logout(request)

    return redirect('login')
