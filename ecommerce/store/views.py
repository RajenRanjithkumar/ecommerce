from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages  
from django.http import JsonResponse
import json
import datetime
from .utils import cookieCart, cartData, guestOrder
from .forms import CreateCustomerForm, ProductForm, ImageForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm  #djangos default form
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404
from django.db.models import Q # to include or/and condition for queries 

from django.forms import modelformset_factory # for uploading multiple images


# Create your views here.

#https://www.youtube.com/watch?v=kH2FOWuA4uI&list=PL-51WBLyFTg0omnamUjL1TCVov7yDTRng&index=6
#49:48






def store(request):

    data = cartData(request)
    order = data['order']
    items = data['items']
    cartItems = data['cartItems']
    siteUser = "customer"

    categories = Product.CHOICES

    print(categories)

    #search for products
    q = request.GET.get('q') if request.GET.get('q') != None else '' 
     #print(type(int(category)))
    products = Product.objects.filter(
        Q(name__icontains = q)|
        Q(category__icontains = q)

        
    )

    # Filter products according to categories
    category = request.GET.get('category') if request.GET.get('category') != None else ''
    if category:
        print(type(category))
        products = Product.objects.filter(

            category = category
        )

    

    #products = Product.objects.all()
    context = {'products': products, 
               'cartItems': cartItems, 
               'siteUser':siteUser, 
               'categories': categories}


    return render(request, 'store/store.html', context)




def productDetails(request, pk):

    data = cartData(request)
    order = data['order']
    items = data['items']
    cartItems = data['cartItems']
    siteUser = "customer"

    #navbar 
    categories = Product.CHOICES

    product = Product.objects.get(id = pk)
    otherImages = Images.objects.filter(product = product)
    print(otherImages)
    

    context = {'siteUser':siteUser, 'cartItems':cartItems, 'product': product, 'otherImages': otherImages, 'categories':categories}

    return render(request, 'store/product_details.html', context)



def cart(request):

    data = cartData(request)
    order = data['order']
    items = data['items']
    cartItems = data['cartItems']
    siteUser = "customer"

    #Logic moved to ulits.py 2
    
            

    context = {'items': items, 'order': order, 'cartItems': cartItems, 'siteUser':siteUser}
    return render(request, 'store/cart.html', context)

def checkout(request):


    data = cartData(request)
    order = data['order']
    items = data['items']
    cartItems = data['cartItems']
    siteUser = "customer"

    #logic moved to utils.py
    
    context = {'items': items, 
               'order': order, 
               'cartItems': cartItems , 
               "shipping": False, 
               "siteUser": siteUser}

    
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
    order.trasaction_id = int(trasaction_id)

    # to cross check the total cost

    print(round(total))
    print(round(order.get_cart_total))
    if round(total) == round(order.get_cart_total):
        order.complete = True

    print(order.trasaction_id)
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


@login_required(login_url='login')
def userOrders(request):
    data = cartData(request)
    cartItems = data['cartItems']
    siteUser = "customer"
    
    customer_order_items = []
    try:
        customer_orders = Order.objects.filter(customer = request.user.customer)
        
        for order in customer_orders:
            order_items = OrderItem.objects.filter(order=order)
            customer_order_items.extend(order_items)
        
        #print(customer_orders)
        print(customer_order_items)
    except Exception as e:
        print(e)
    
    

    
    context = {"siteUser": siteUser, "cartItems":cartItems, "orders": customer_order_items}
    return render(request, 'store/user_orders.html', context)
    
    
    
def customerOrderDetails(request, pk):
    
    
    orderItem = OrderItem.objects.get(id = pk)
    shippingAddress = ShippingAddress.objects.get(order = orderItem.order)
    trakingStatus  = ProductTracking.objects.get(customer = orderItem.order.customer, orderItem = orderItem)
    
    
    context = {"orderItem":orderItem, "shippingAddress": shippingAddress, "shipped": trakingStatus}
    return render(request, 'store/customer_order_details.html', context)



#User Registration and Authentication
def loginUser(request):

    
    data = cartData(request)
    order = data['order']
    items = data['items']
    cartItems = data['cartItems']
            


    page = "login"

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # storage = messages.get_messages(request)
        # storage.used = True

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
                    messages.error(request, None)
                    return redirect('store')
                else:
                    messages.error(request, "Username or password does not exist")
            except Customer.DoesNotExist:
                customerObj = None
                #messages.error(request, "Username or password does not exist")
            

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
            
            login(request, user)
            return redirect('store')
        else:

            messages.error(request, "An error occured during registration")

    context = {'form': form}
    return render(request, 'store/login.html', context) 


def logoutUser(request):
    
    logout(request)

    return redirect('login')





# Seller routes



def loginSeller(request):

    page = 'login'

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        
        if username != '' and password != '':
            try:
                user = User.objects.get(username = username)
                # seller = Seller(user=user)
                # seller.save()
                seller = authenticate(request, username=username, password=password)
                if seller is not None:

                    try:
                        sellerObj = Seller.objects.get(user = seller)
                        #print("Is customer", customerName.name)
                        if sellerObj.name is not None:

                            login(request, user)
                            messages.error(request, None)
                            return redirect('seller_products')
                
                    # else:
                    #     messages.error(request, "Sellername or password does not exist")

                    except Seller.DoesNotExist:
                        #sellerObj = None
                        messages.error(request, "Sellername or password does not exist")
                else:
                    messages.error(request, "Sellername or password incorrect")

            except:

                messages.error(request, " Seller does not exist ") #Django flash messages
        else:
            messages.error(request, " Username or password cannot be empty ") #Django flash messages


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



@login_required(login_url='seller_login')
def sellerProducts(request):


     #search for products
    q = request.GET.get('q') if request.GET.get('q') != None else '' 
    products = Product.objects.filter(
        Q(name__icontains = q), 
        seller = request.user.seller,
        
    )


    #products = Product.objects.filter(seller = request.user.seller)

    context = {"products":products}

    return render(request, "store/seller_products.html", context)

@login_required(login_url='seller_login')
def sellerAddProduct(request):

    ImageFormSet = modelformset_factory(Images, form=ImageForm, extra=3)

    product_form = ProductForm()
    formset = ImageFormSet(queryset=Images.objects.none())
    
    
    if request.method == 'POST':
        
        product_form = ProductForm(request.POST, request.FILES)
        formset = ImageFormSet(request.POST, request.FILES, queryset=Images.objects.none())

        if product_form.is_valid() and formset.is_valid():
            
            #product = form.save()

            product_instance = Product.objects.create(

                name = product_form.cleaned_data['name'],
                price = product_form.cleaned_data['price'],
                brand = product_form.cleaned_data['brand'],
                description = product_form.cleaned_data['description'],
                digital = product_form.cleaned_data['digital'],
                image = product_form.cleaned_data['image'],
                seller = request.user.seller,
                category = product_form.cleaned_data['category']

            )

            
            
            for form in formset.cleaned_data:
                #this helps to not crash if the user   
                #do not upload all the photos
                if form:
                    image = form['images']
                    photo = Images(product = product_instance, images=image)
                    photo.save()

             # use django messages framework
            messages.success(request,
                             "Yeeew, check it out on the home page!")


            #return JsonResponse('Item was added', safe=False)
            return redirect("seller_products")
       




    context = {"form": product_form, 'formset': formset}
    

    return render(request, "store/seller_add_product.html", context)

@login_required(login_url='seller_login')
def sellerUpdateProduct(request, pk):

    ImageFormSet = modelformset_factory(Images, form=ImageForm, extra=3)

    product = Product.objects.get(id = pk)
    
    
    if request.user != product.seller.user:
        return JsonResponse("Product is sold by someone else", safe=False)
        
    
    #fill the form with existing data
    product_form = ProductForm(instance=product)
    formset = ImageFormSet(queryset=Images.objects.filter(product = product))

    # update the form
    if request.method == 'POST':

        product_form = ProductForm(request.POST, request.FILES, instance=product)
        formset = ImageFormSet(request.POST, request.FILES, queryset=Images.objects.filter(product = product))

        if product_form.is_valid() and formset.is_valid():
            
            product = product_form.save()

            formset.save()

            # Product.objects.create(

            #     name = form.cleaned_data['name'],
            #     price = form.cleaned_data['price'],
            #     digital = form.cleaned_data['digital'],
            #     image = form.cleaned_data['image'],
            #     seller = request.user.seller
            # )

            #return JsonResponse('Item was added', safe=False)
            return redirect("seller_products")


    context = {'form': product_form, 'formset': formset}
    return render(request, "store/seller_add_product.html", context)
    # return JsonResponse(product.price, safe=False)

@login_required(login_url='seller_login')
def sellerDeleteProduct(request, pk):

    product = Product.objects.get(id = pk)

    
    if product:
        print(product.name + " deleted successfully!!")
        product.delete()
        
    
    
    return redirect("seller_products")

@login_required(login_url='seller_login')
def sellerOrders(request):
    
    products_by_seller = Product.objects.filter(seller= request.user.seller)
    orders = OrderItem.objects.filter(product__in=products_by_seller)
    #orders_by_seller = [order_item.order for order_item in order_items_for_products]
    print("Tesetin", orders)
    
    context = {"orders": orders}
    return render(request, "store/seller_orders.html", context)

@login_required(login_url='seller_login')
def sellerOrderDetails(request, pk):
    
    #Get the order details
    orderItem = OrderItem.objects.get(id = pk)
    shippingAddress = ShippingAddress.objects.get(order = orderItem.order)
    trakingInstance, created = ProductTracking.objects.get_or_create(customer = orderItem.order.customer, orderItem = orderItem)
    #shipped = trakingInstance.orderSent
    #itemWisePrice = orderItem.quantity * orderItem.product.price
    print((trakingInstance.orderSent))
    print(trakingInstance.trackingID)
    
    #Get the courier details from front end
    if request.method == 'POST':
        
        courierName = request.POST.get("Courier_name")
        trackingId = request.POST.get("tracking_id")
        
        
        print(courierName, trackingId)
        
        if courierName != '' and trackingId != '':
            
           
                
                trakingInstance = ProductTracking.objects.filter(orderItem = orderItem).update(courierName = courierName, trackingID = trackingId, orderSent = True)
            
                # trakingInstance = ProductTracking.objects.update(
                      
                #     customer = orderItem.order.customer,
                #     orderItem = orderItem,
                #     courierName = courierName,
                #     trackingID = trackingId,
                #     orderSent = True
                # )
                
                return redirect('seller_orders')
                
            
                
            
        else:
            messages.error(request, "Order details cannot be empty")
    
    
        #print(trakingInstance.orderSent)


    
    context = {"orderItem":orderItem, "shippingAddress": shippingAddress, "shipped": trakingInstance}
    
    return render(request, 'store/seller_order_details.html', context)
    

def logoutSeller(request):
    
    logout(request)

    return redirect('seller_login')
