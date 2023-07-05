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
from django.shortcuts import get_object_or_404


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
            #customerName = Customer.objects.get(user = user)
           
        except:

            messages.error(request, " User does not exist ") #Django flash messages
    else:
        messages.error(request, " Username or password cannot be empty ") #Django flash messages

    
    customer = authenticate(request, username=username, password=password)
    
    

    if customer is not None:

        try:
            customerObj = Customer.objects.get(user = customer)

            #customerObj = get_object_or_404(Customer, user = customer)
            print("Is customer", customerObj.name)
            if customerObj.name is not None:
                login(request, user)
                return redirect('store')
            else:
                messages.error(request, "Username or password does not exist")
        except Customer.DoesNotExist:
            customerObj = None
            #messages.error(request, "Username or password does not exist")
        #h
    
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



def loginSeller(request):

    page = 'login'

    
    username = request.POST.get('username')
    password = request.POST.get('password')

    
    if username != '' and password != '':
        try:
            user = User.objects.get(username = username)
            # seller = Seller(user=user)
            # seller.save()
        except:

            messages.error(request, " Seller does not exist ") #Django flash messages
    else:
        messages.error(request, " Username or password cannot be empty ") #Django flash messages

    
    seller = authenticate(request, username=username, password=password)

    if seller is not None:

        try:
            sellerObj = Seller.objects.get(user = seller)
            #print("Is customer", customerName.name)
            if sellerObj.name is not None:

                login(request, user)
                return redirect('seller_profile')
            
            else:
                messages.error(request, "Sellername or password does not exist")

        except Seller.DoesNotExist:
            #sellerObj = None
            messages.error(request, "Sellername or password does not exist")



    else:
        messages.error(request, "Sellername or password does not exist")

    context = {"page": page}
    return render(request, 'store/seller_login.html', context)

def registerSeller(request):

    form = CreateCustomerForm()


    if request.method == 'POST':
        form = CreateCustomerForm(request.POST)
        if form.is_valid():
            
            user = form.save(commit=False)

            
            user.username = user.username.lower()
            user.save()

            # #login(request, user)

            Seller.objects.create(

                user = user,
                name = user.username,
                email = user.email

            )
            return redirect('seller_login')
        else:

            messages.error(request, "An error occured during registration")

    context = {'form':form}
    return render(request, 'store/seller_login.html', context)


def sellerProfile(request):

    context = {}

    return render(request, "store/seller_profile.html", context)




def cart(request):

    data = cartData(request)
    order = data['order']
    items = data['items']
    cartItems = data['cartItems']

    #Logic moved to ulits.py 2
    
            

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)

def checkout(request):

    data = cartData(request)
    order = data['order']
    items = data['items']
    cartItems = data['cartItems']

    #logic moved to utils.py
    
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
