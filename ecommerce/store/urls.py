from django.urls import path
from . import views

urlpatterns = [

    path('', views.store, name='store'), # home page
    path('login/', views.loginUser, name='login'),
    path('register/', views.registerUser, name='register'),

    path('seller_login/', views.loginSeller, name='seller_login'),
    path('seller_register/', views.registerSeller, name='seller_register'),

     path('seller_profile/', views.sellerProfile, name='seller_profile'),


    path('logout/', views.logoutUser, name='logout'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('update_item/', views.updateItem, name='update_item'),
    path('process_order/', views.processOrder, name='process_order')



]