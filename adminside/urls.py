from django.urls import path
from . views import admin_home, admin_login, block, users, product_list, category, block, unblock, add_new_product 
from . views import add_new_category, update_category, update_product, delete_product, delete_category, admin_logout
from. views import address_list, order_list, update_order, submit_order, sales, export_to_pdf, export_to_excel
from. views import offer_page, add_new_coupon, coupon_page, category_offer_page, add_category_offer, product_offer_page
from. views import add_product_offer, delete_product_offer, delete_category_offer, delete_coupon, export_to_csv

urlpatterns = [
    path('admin_home', admin_home, name='admin_home'),
    path('admin_login', admin_login, name='admin_login'),
    path('admin_logout', admin_logout, name='admin_logout'),
    path('users', users, name='users'),
    path('product_list', product_list, name='product_list'),
    path('address_list', address_list, name='address_list'),
    path('order_list', order_list, name='order_list'),
    path('category', category, name='category'),
    path('block/<int:id>', block, name='block'),
    path('unblock/<int:id>', unblock, name='unblock'),
    path('add_new_product', add_new_product, name='add_new_product'),
    path('add_new_category', add_new_category, name='add_new_category'),
    path('update_category/<int:id>', update_category, name='update_category'),
    path('update_product/<int:id>', update_product, name='update_product'),
    path('delete_product/<int:id>', delete_product, name='delete_product'),
    path('delete_category/<int:id>', delete_category, name='delete_category'),
    path('update_order/<int:id>', update_order, name='update_order'),
    path('submit_order/<int:id>', submit_order, name='submit_order'),
    path('sales', sales, name='sales'),
    path('export_to_pdf', export_to_pdf, name='export_to_pdf'),
    path('export_to_excel', export_to_excel, name='export_to_excel'),
    path('offer_page', offer_page, name='offer_page'),
    path('add_new_coupon', add_new_coupon, name='add_new_coupon'),
    path('coupon_page', coupon_page, name='coupon_page'),
    path('category_offer_page', category_offer_page, name='category_offer_page'),
    path('add_category_offer', add_category_offer, name='add_category_offer'),
    path('product_offer_page', product_offer_page, name='product_offer_page'),
    path('add_product_offer', add_product_offer, name='add_product_offer'),
    path('delete_product_offer/<int:id>', delete_product_offer, name='delete_product_offer'),
    path('delete_category_offer/<int:id>', delete_category_offer, name='delete_category_offer'),
    path('delete_coupon/<int:id>', delete_coupon, name='delete_coupon'),
    path('export_to_csv', export_to_csv, name='export_to_csv'),
]