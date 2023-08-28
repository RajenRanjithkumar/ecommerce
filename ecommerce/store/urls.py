from django.urls import path
from . import views

urlpatterns = [

    path('', views.store, name='store'), # home page
    path('login/', views.loginUser, name='login'),
    path('register/', views.registerUser, name='register'),
    path('product/<str:pk>', views.productDetails, name='product'),

    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('update_item/', views.updateItem, name='update_item'),
    path('process_order/', views.processOrder, name='process_order'),
    path('logout/', views.logoutUser, name='logout'),

    path('seller_login/', views.loginSeller, name='seller_login'),
    path('seller_register/', views.registerSeller, name='seller_register'),

    path('seller_products/', views.sellerProducts, name='seller_products'),
    path('seller_products/orders/', views.sellerOrders, name='seller_orders'),
    path('seller_products/orders/<str:pk>', views.sellerOrderDetails, name='seller_order_details'),
    
    
    path('seller_add_product/', views.sellerAddProduct, name='seller_add_product'),
    path('seller_update_product/<str:pk>', views.sellerUpdateProduct, name='seller_update_product'),
    path('seller_delete_product/<str:pk>', views.sellerDeleteProduct, name='seller_delete_product'),
    path('seller_logout/', views.loginSeller, name='seller_logout'),
    
]