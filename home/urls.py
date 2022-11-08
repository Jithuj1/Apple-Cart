from atexit import register
from django.urls import path, include
from . import views 
from .views import login, otp_page, register, product, home, cart, logout, otp_login, detailed_view, add_cart
from .views import remove_cart, remove_cart_item, checkout, profile, contact, my_orders, update_cart_data
from .views import product_searach, wishlist, wish, delete_wish, download, cancel_order, return_order

urlpatterns = [
    path('', home, name='home'),
    path('login', login, name='login'),
    path('register', register, name='register'),
    path('product', product, name='product'),
    path('cart', cart, name='cart'),
    path('checkout', checkout, name='checkout'),
    path('add_cart/<int:id>', add_cart, name='add_cart'),
    path('remove_cart/<int:id>', remove_cart, name='remove_cart'),
    path('remove_cart_item/<int:id>', remove_cart_item, name='remove_cart_item'),
    path('otp_login', otp_login, name='otp_login'),
    path('otp_page',  otp_page, name='otp_page'),
    path('logout', logout, name='logout'),
    path('detailed_view/<int:id>',detailed_view, name='detailed_view'),
    path('profile',  profile, name='profile'),
    path('contact',  contact, name='contact'),
    path('my_orders',  my_orders, name='my_orders'),
    path('update_cart_data',  update_cart_data, name='update_cart_data'),
    path('product_searach',  product_searach, name='product_searach'),
    path('wishlist/<int:id>',wishlist, name='wishlist'),
    path('wish',wish, name='wish'),
    path('delete_wish/<int:id>', delete_wish, name='delete_wish'),
    path('cancel_order/<int:id>', cancel_order, name='cancel_order'),
    path('return_order/<int:id>', return_order, name='return_order'),
    path('download/<int:productID>', download, name='download'),


]
