from .views import *
from django.urls import path, include


urlpatterns = [
    path('add_new_address', add_new_address, name='add_new_address'),
    path('place_order', place_order, name="place_order"),
    path('payments', payments, name="payments"),
    path('razor_pay', razor_pay, name="razor_pay"),
    path('cod', cod, name="cod"),
    path('apply_coupon', apply_coupon, name="apply_coupon"),
    path('delete_address/<int:id>', delete_address, name='delete_address')

]
