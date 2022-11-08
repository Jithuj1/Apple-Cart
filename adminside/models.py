from unicodedata import category
from django.db import models
from home.models import *

class SalesReport(models.Model):
    productName = models.CharField(max_length=100)
    categoryName = models.CharField(max_length=100)
    date = models.DateField()
    quantity = models.IntegerField()
    productPrice = models.FloatField()


class Coupan(models.Model):
    coupan_code=models.CharField(max_length=25)
    start_date_and_time=models.DateTimeField()
    end_date_and_time=models.DateTimeField()
    discount_amount=models.CharField(max_length=5,blank=True)
    discount_percentage=models.CharField(max_length=5,blank=True)


class Coupan_applied(models.Model):
    coupan=models.ForeignKey(Coupan, on_delete =models.CASCADE)
    user=models.ForeignKey(User_data, on_delete =models.CASCADE)


class CategoryOffer(models.Model):
    cid = models.ForeignKey(category_details,on_delete=models.CASCADE)
    valid_till = models.DateField()
    Name = models.CharField(max_length=100)
    percentage = models.IntegerField()
    description = models.TextField()
    status = models.BooleanField(max_length=20,default=True)


class ProductOffer(models.Model):
    pid = models.ForeignKey(product_data,on_delete=models.CASCADE)
    valid_till = models.DateField()
    Name = models.CharField(max_length=100)
    percentage = models.IntegerField()
    description = models.TextField()
    status = models.BooleanField(max_length=20,default=True)