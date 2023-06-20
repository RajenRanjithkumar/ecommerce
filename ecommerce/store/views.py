from django.shortcuts import render

# Create your views here.

#https://www.youtube.com/watch?v=_ELCMngbM0E&list=PL-51WBLyFTg0omnamUjL1TCVov7yDTRng
#19:13

def store(request):

    context = {}
    return render(request, 'store/store.html', context)

def cart(request):

    context = {}
    return render(request, 'store/cart.html', context)

def checkout(request):

    context = {}
    return render(request, 'store/checkout.html', context)