from django.db import models
from home.models import User_data, product_data, category_details

# Create your models here.

class Address(models.Model):
    user = models.ForeignKey(User_data, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    house_name = models.CharField( max_length=50)
    city = models.CharField( max_length=50)
    pin = models.CharField( max_length=50)
    phone = models.CharField( max_length=50)
    email = models.CharField( max_length=50)
    district = models.CharField( max_length=50)
    state = models.CharField( max_length=50)
    country = models.CharField( max_length=50)
    full_address = models.TextField()
    address_id = models.CharField( max_length=50)

    def __str__(self):
        return self.user.name
    

class Payment(models.Model):
    user = models.ForeignKey(User_data, on_delete=models.CASCADE)
    payment_id = models.CharField( max_length=50)
    payment_method = models.CharField( max_length=100)
    amount_paid = models.CharField( max_length=50)
    status = models.CharField( max_length=50)
    created_at = models.DateField(  auto_now_add=True)

    def __str__(self):
        return self.payment_id
    

class Order(models.Model):
    STATUS=(
        ('New','New'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(User_data, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null= True)
    order_number = models.CharField( max_length=50)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    order_note = models.CharField( max_length=50, blank = True)
    order_total = models.FloatField()
    tax = models.FloatField()
    status = models.CharField(max_length=50, choices= STATUS, default='New')
    ip = models.CharField( max_length=50, blank=True)
    is_ordered = models.BooleanField( default=False)
    created_at = models.DateField( auto_now_add=True)
    updated_at = models.DateField( auto_now=True)
    payment_method=models.CharField(max_length=50, default=True)

    def __str__(self):
        return self.user.name


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank = True, null=True)
    user = models.ForeignKey(User_data, on_delete=models.CASCADE)
    Product = models.ForeignKey(product_data, on_delete=models.CASCADE)
    category = models.ForeignKey(category_details, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, default='Delivered')
    quantity = models.IntegerField()
    product_price = models.FloatField()
    product_name = models.CharField( max_length=50, default ='Name')
    ordered = models.BooleanField(default= False)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.product.Product_name
    

class WishList(models.Model):
    user = models.ForeignKey(User_data, on_delete=models.CASCADE)
    Product = models.ForeignKey(product_data, on_delete=models.CASCADE)



    

    


    