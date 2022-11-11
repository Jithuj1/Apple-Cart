from email.policy import default
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# Create your models here.

class MyAccountManager(BaseUserManager):
    def create_user(self, name, email, username, phone,password=None):
        if not email:
            raise ValueError('User must have an email address')

        if not username:
            raise ValueError('User must have an username')

        user = self.model(
            email = self.normalize_email(email),
            username = username,
            name = name,
            phone = phone,
        )

        user.set_password(password)
        user.save(using=self._db)
        
        return user

    def create_superuser(self, phone, email, username ,password,name):
        user=self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
            name = name,
            phone = phone,
        )
        
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user


class User_data(AbstractBaseUser):
    name = models.CharField(max_length=255)    
    phone = models.CharField(max_length=20)   
    email = models.EmailField(max_length=254) 
    gender = models.CharField(max_length=20)
    username = models.TextField(max_length=50, unique= True)
    password = models.TextField()
    confirm_password = models.TextField()
    status = models.BooleanField(default=True, blank=True)


    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin  = models.BooleanField(default=False)
    is_staff   = models.BooleanField(default=False)
    is_active   = models.BooleanField(default=True)
    is_superadmin   = models.BooleanField(default=False)


    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name','phone', 'email']
    

    objects = MyAccountManager()


    def _str_(self):
        return self.username

    
    def has_perm(self, perm, obj=None):
        return self.is_admin

    
    def has_module_perms(self, add_label):
        return True


class product_data(models.Model):
    product_ID = models.CharField(max_length=20)
    Product_name = models.CharField(max_length=50)
    Product_dis = models.TextField()
    Product_price = models.IntegerField()
    discount_price =models.IntegerField(default='001')
    discount_percentage =models.IntegerField(default='0')
    ram = models.CharField(max_length=20)
    storage = models.CharField(max_length=25)
    type = models.CharField(max_length=20)
    image1 = models.ImageField(upload_to = 'uploads', blank = True)
    image2 = models.ImageField(upload_to = 'uploads', blank = True) 
    image3 = models.ImageField(upload_to = 'uploads', blank = True)
    image4 = models.ImageField(upload_to = 'uploads', blank = True) 
    category_id= models.ForeignKey('category_details', on_delete= models.CASCADE)
    stoke_status = models.CharField(max_length=50, default='100', null = True)


class Cart(models.Model):
    cart_id = models.CharField(max_length=255, blank=True)
    date_added = models.DateField(auto_now_add= True)

    def __str__(self):
        return self.cart_id


class CartItem(models.Model):
    user=models.ForeignKey(User_data, on_delete=models.CASCADE, null= True)
    product = models.ForeignKey(product_data, on_delete= models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete= models.CASCADE, null=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        return self.product.Product_price * self.quantity

    def __str__(self):
        return self.product


class category_details(models.Model):
    category_id = models.CharField(max_length=20)
    category_name = models.CharField(max_length=50)
    category_dis = models.CharField(max_length=255)
    img = models.ImageField(upload_to='static/uploads', blank = True)





