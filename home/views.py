
from ast import Not
from gc import get_objects
import imp
import re
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from adminside.models import Coupan
from adminside.models import CategoryOffer
from adminside.models import ProductOffer
from .models import User_data, Cart, CartItem, product_data, category_details
from orders.models import *
import random
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import *
from twilio.rest import Client
from django.contrib.auth import authenticate
from django.contrib import auth
import json
from xhtml2pdf import pisa
from django.http import HttpResponse
from django.template.loader import get_template
import io
import datetime
from django.conf import settings




def home(request):
    if 'uname' in request.session:
        a=User_data.objects.get(username = request.session.get('uname'))
        return render(request, 'home.html', {'data': a})
    else:
        return render(request, 'home.html')


def login(request):
    if request.method == 'POST':
        uname = request.POST['username']
        pword = request.POST['password'] 
        if uname == '' or pword == '':
            messages.error(request, " blank space not allowed")
            return redirect('login')
        user = authenticate(username=uname, password=pword)
        if user is not None:
            value = User_data.objects.filter(username=uname)
            for i in value:
                if i.is_superadmin is False:
                    auth.login(request, user)
                    print('jithu is here')
                    try:
                        print('jithu is here2')
                        print('jithu is here3')
                        guest_cart_item = CartItem.objects.filter(user__isnull=True)  
                        print('jithu is here4')                 
                        user_cart_item=CartItem.objects.filter(user=user)
                        print('jithu is here5')
                        if user_cart_item:
                            if guest_cart_item:
                                for guest in guest_cart_item:
                                    try:
                                        product=CartItem.objects.get(user=user, product=guest.product)                                    
                                        if product:
                                            n = guest.quantity
                                            m = product.quantity
                                            k = n+m
                                            if k <10:
                                                product.quantity=k
                                                product.save()
                                                guest.delete()
                                            else:
                                               product.quantity=10 
                                               product.save()
                                               guest.delete()
                                    except:
                                        pass
                            else:
                                print("hello")
                                pass
                        else:
                            print('guest cart')
                            for guest in guest_cart_item:
                                guest.user=user
                                guest.save()
                    except:
                        pass
                    request.session['uname'] = uname
                    return redirect(home)       
                else:
                    messages.error(request, "Only for users")
                    return redirect(login)
            
        else:
            messages.error(request, " incorrect password or username")
            return redirect('login')
    else:
        messages.error(request, " Please enter your password and username")
        return render(request, 'login.html')


def logout(request):
    if 'uname' in request.session:
        del request.session['uname']
        auth.logout(request)
        return redirect('home')     


def register(request):
    if request.method == 'POST':
        name = request.POST['name']
        phone = request.POST['phonenumber']
        email = request.POST['email']
        gender = request.POST['inlineRadioOptions']
        username = request.POST['username']
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')
        print('password',password,cpassword)
        if User_data.objects.filter(username=username).exists():
            messages.info(request, 'Username already taken')
            return redirect('register')
        elif User_data.objects.filter(email=email).exists():
            messages.info(request, 'Email already taken')
            return redirect('register')
        elif User_data.objects.filter(phone=phone).exists():
            messages.info(request, 'Phone number already taken')
            return redirect('register')
        elif name == '' or phone == '' or gender == '' or password == '' or cpassword == '' or username == '' or email == '':
            messages.info(request, ' blank space not allowed')
            return redirect('register')
        elif password != cpassword:
            messages.info(request, 'password is not same')
            return redirect('register')
        else:
            user = User_data.objects.create_user(name = name, phone = phone, email = email, username = username, password =  password,)
            user.save(); 
            print('user created')
            messages.info(request, 'user created')
            return redirect(login)

    else:
        return render(request, 'register.html')


def product(request):
    k = product_data.objects.all()
    if k :
        for i in k :
            print('entering here')
            j = OrderProduct.objects.filter(Product = i.id)
            for l in j :
                l.product_name=i.Product_name
                l.save()
    if 'uname' in request.session:
        categories = None
        products = None
        
        if request.method == "POST":
            categories=category_details.objects.all()
            value = request.session.get('uname')
            user=User_data.objects.get(username = value)

            search_data = request.POST.get('search')
            products=product_data.objects.filter(Product_name__icontains=search_data)
            paginator=Paginator(products, 6)
            page = request.GET.get('page')
            paged_products = paginator.get_page(page)
            product_count = products.count()
            

        else:
            categories=category_details.objects.all()
            value = request.session.get('uname')
            user=User_data.objects.get(username = value)
            products=product_data.objects.all()
            paginator=Paginator(products, 6)
            page = request.GET.get('page')
            paged_products = paginator.get_page(page)
            product_count = products.count()
            
        a=product_data.objects.all()
        for i in a:
            i.discount_price=i.Product_price
            i.discount_percentage = 0
            i.save()
        now=datetime.datetime.now().strftime('%Y-%m-%d')
        print(now)
        products=product_data.objects.all()
        for k in products:
            try:
                p_offer=ProductOffer.objects.get(valid_till__gte=now, pid=k.id)
                try:
                    c_offer=CategoryOffer.objects.get( valid_till__gte=now, cid=k.category_id)
                    if int(p_offer.percentage) > int(c_offer.percentage):
                        calculating_discount=int(p_offer.percentage)*k.Product_price/100
                        k.discount_price=k.Product_price-calculating_discount
                        k.discount_percentage=p_offer.percentage
                        k.save()
                    elif int(p_offer.percentage) < int(c_offer.percentage):
                        calculating_discount=int(c_offer.percentage)*k.Product_price/100
                        k.discount_price=k.Product_price-calculating_discount
                        k.discount_percentage=c_offer.percentage
                        k.save()
                    elif int(p_offer.percentage) == int(c_offer.percentage):
                        calculating_discount=int(p_offer.percentage)*k.Product_price/100
                        k.discount_price=k.Product_price-calculating_discount
                        k.discount_percentage=p_offer.percentage
                        k.save()
                except:
                    p_offer=ProductOffer.objects.get( valid_till__gte=now,pid=k.id)
                    calculating_discount=int(p_offer.percentage)*k.Product_price/100
                    k.discount_price=k.Product_price-calculating_discount
                    k.discount_percentage=p_offer.percentage
                    k.save()
            except:
                try:
                    c_offer=CategoryOffer.objects.get( valid_till__gte=now, cid=k.category_id)
                    calculating_discount=int(c_offer.percentage)*k.Product_price/100
                    k.discount_price=k.Product_price-calculating_discount
                    k.discount_percentage=c_offer.percentage
                    k.save()
                except:
                    pass

        context = { 
                'categories':categories,
                'user' : user, 
                'product_details' : paged_products,
                'product_count' : product_count,
            }
        return render(request, 'products.html', context)

    else:
        categories = None
        products = None
        
        if request.method == "POST":
            categories=category_details.objects.all()

            search_data = request.POST.get('search')
            products=product_data.objects.filter(Product_name__icontains=search_data)
            paginator=Paginator(products, 6)
            page = request.GET.get('page')
            paged_products = paginator.get_page(page)
            product_count = products.count()
            
        else:
            categories=category_details.objects.all()
            products=product_data.objects.all()
            paginator=Paginator(products, 6)
            page = request.GET.get('page')
            paged_products = paginator.get_page(page)
            product_count = products.count()
            
        a=product_data.objects.all()
        for i in a:
            i.discount_price=i.Product_price
            i.discount_percentage = 0
            i.save()
        now=datetime.datetime.now().strftime('%Y-%m-%d')
        print(now)
        products=product_data.objects.all()
        for k in products:
            try:
                p_offer=ProductOffer.objects.get(valid_till__gte=now, pid=k.id)
                try:
                    c_offer=CategoryOffer.objects.get( valid_till__gte=now, cid=k.category_id)
                    if int(p_offer.percentage) > int(c_offer.percentage):
                        calculating_discount=int(p_offer.percentage)*k.Product_price/100
                        k.discount_price=k.Product_price-calculating_discount
                        k.discount_percentage=p_offer.percentage
                        k.save()
                    elif int(p_offer.percentage) < int(c_offer.percentage):
                        calculating_discount=int(c_offer.percentage)*k.Product_price/100
                        k.discount_price=k.Product_price-calculating_discount
                        k.discount_percentage=c_offer.percentage
                        k.save()
                    elif int(p_offer.percentage) == int(c_offer.percentage):
                        calculating_discount=int(p_offer.percentage)*k.Product_price/100
                        k.discount_price=k.Product_price-calculating_discount
                        k.discount_percentage=p_offer.percentage
                        k.save()
                except:
                    p_offer=ProductOffer.objects.get( valid_till__gte=now,pid=k.id)
                    calculating_discount=int(p_offer.percentage)*k.Product_price/100
                    k.discount_price=k.Product_price-calculating_discount
                    k.discount_percentage=p_offer.percentage
                    k.save()
            except:
                try:
                    c_offer=CategoryOffer.objects.get( valid_till__gte=now, cid=k.category_id)
                    calculating_discount=int(c_offer.percentage)*k.Product_price/100
                    k.discount_price=k.Product_price-calculating_discount
                    k.discount_percentage=c_offer.percentage
                    k.save()
                except:
                    pass

        context = { 
                'categories':categories,
                'product_details' : paged_products,
                'product_count' : product_count,
            }
        return render(request, 'products.html', context)
    

def detailed_view(request, id):
    product_details = product_data.objects.get(id = id)
    return render(request, 'detailed_view.html', {'data':product_details})


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart
    
    
def add_cart(request, id):
    if 'uname' in request.session:
        u = request.session.get('uname')
        print(u,"hiii")
        d = User_data.objects.get(username=u)
        print(d.id, 'id')
        product = product_data.objects.get(id = id)
        try:
            cart = Cart.objects.get(cart_id = _cart_id(request))
        except Cart.DoesNotExist:
            cart= Cart.objects.create(
                cart_id = _cart_id(request)
            )
        cart.save()
        try:
            cart = Cart.objects.get(cart_id = _cart_id(request))
            cart_item = CartItem.objects.get(product=product, user=request.user)
            if cart_item.quantity<10:
                cart_item.quantity += 1 
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                cart = cart,
                user=request.user,)
            cart_item.save()
    else:
        product = product_data.objects.get(id = id)
        try:
            cart = Cart.objects.get(cart_id = _cart_id(request))
        except Cart.DoesNotExist:
            cart= Cart.objects.create(
                cart_id = _cart_id(request)
            )
        cart.save()
        try:
            cart_item = CartItem.objects.get(product=product, cart=cart)
            cart_item.quantity += 1 
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                cart = cart,)
            cart_item.save()
    return redirect ('cart')


def cart(request, total=0, quantity=0, cart_item=None): 
    cart_items=0
    tax=0
    grand_total=0
    if request.user.is_authenticated:
        try:
            current_user=request.user
            # cart=Cart.objects.get(cart_id =_cart_id(request))
            cart_items=CartItem.objects.filter(user=request.user, is_active=True)
            # print("cartitemmmmm",cart_items)
            for cart_item in cart_items:
                total += (cart_item.product.discount_price * cart_item.quantity)
                quantity += cart_item.quantity
            tax = 0.01 * total
            grand_total = total+tax 
        except ObjectDoesNotExist:
            print('entered in the except block')
    else:
        try:
            cart=Cart.objects.get(cart_id =_cart_id(request))
            cart_items=CartItem.objects.filter(cart=cart, is_active=True)
            for cart_item in cart_items:
                total += (cart_item.product.discount_price * cart_item.quantity)
                quantity += cart_item.quantity
            tax = 0.01 * total
            grand_total = total+tax 
        except ObjectDoesNotExist:
            pass
        
    context ={
        'total':total,
        'quantity':quantity,
        'cart_items': cart_items,
        'tax' : tax,
        'grand_total':grand_total,
        }
    return render(request, 'cart.html', context )


def remove_cart(request, id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(product_data, id= id)
    cart_item = CartItem.objects.get(product=product, user=request.user, cart=cart)
    if cart_item.quantity >1:
        cart_item.quantity -=1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect ('cart')


def remove_cart_item(request, id):
    product = get_object_or_404(product_data, id=id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.filter(product=product, user=request.user)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.filter(product=product, cart=cart)
      
    cart_item.delete()
    return redirect('cart')


def checkout(request, total=0, quantity=0, cart_item=None):
    if 'uname' in request.session:
        cart_items=0
        tax=0
        grand_total=0
        address=0
        username=request.session.get('uname')
        user_name=User_data.objects.get(username=username)
        address=Address.objects.filter(user=user_name.id)
        try:
            cart_items=CartItem.objects.filter(user=request.user, is_active=True)
            for cart_item in cart_items:
                total += (cart_item.product.discount_price * cart_item.quantity)
                quantity += cart_item.quantity
            if 'coupan_session' in request.session:
                coupan_session=request.session.get('coupan_session')
                dis = Coupan.objects.get(id=coupan_session)
                value = dis.discount_percentage
                discount =  total*(int(value)/100)
                discount_price = total-discount  
            else:
                discount =0
                discount_price = total-discount
                
            tax = 0.01 * discount_price
            grand_total = discount_price+tax 
        except ObjectDoesNotExist:
            pass
        
        context ={
            'total':total,
            'quantity':quantity,
            'cart_items': cart_items,
            'discount_price':discount_price,
            'tax' : tax,
            'discount':discount,
            'grand_total':grand_total,
            'address':address
            }
        return render(request, 'checkout.html', context)
    else:
        return redirect(login)


def otp_login(request):
    if request.method == 'POST':
        no = request.POST.get('phone')
        if User_data.objects.filter(phone=no).exists():
            request.session['phone']=no
            otp = random.randint(1000, 9999)
            account_sid = settings.AccountSid 
            auth_token = settings.AuthToken
            client =Client(account_sid,auth_token)
            msg = client.messages.create(
                body = f"Your OTP is {otp}",
                from_ = "+13024059502",
                to = "+916282224185"
            )
            request.session['otp']=otp
            return redirect(otp_page)
        else:
            messages.info(request, 'invalid mobile number')
            return redirect('otp_login')

    return render( request, 'otplogin.html')


def otp_page(request):
    if request.method=='POST':
        value = request.POST['value']
        otp=request.session.get('otp')
        phone=request.session.get('phone')
        print(otp,value, phone, 'otp,nvlaue')
        print(type(otp),type(value))
        if(int(value)==otp):
            a=User_data.objects.get(phone = phone)
            request.session['uname'] = a.username
            return render(request, 'home.html', {'data': a})
    return render(request, 'otppage.html')


def profile(request):
    if 'uname' in request.session:
        return render(request, 'profile.html')
    else:
        return redirect(login)


def my_orders(request):
    if 'uname' in request.session:
        current_user=request.user
        order_details=OrderProduct.objects.filter(user=current_user)
        paginator=Paginator(order_details, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        context={
        'paged_products':paged_products, 
        }
        return render(request, 'orders.html', context)
    else:
        return redirect(login)


def cancel_order(request, id):
    orderproduct =OrderProduct.objects.get(id = id)
    orderproduct.status= 'Order Canceled'
    orderproduct.save()
    return redirect(my_orders)


def return_order(request, id):
    orderproduct =OrderProduct.objects.get(id = id)
    orderproduct.status= 'Return Requested'
    orderproduct.save()
    return redirect(my_orders)


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return


def download(request,productID):
    print(productID)
    v=OrderProduct.objects.get(id=productID)
    mydict={
        'customerName':v.user.name,
        'customerEmail':v.user.email,
        'customerMobile':v.user.phone,
        'shipmentAddress':v.order.address.full_address,
        'orderStatus':v.payment.status,
        'productimage':v.Product.image1,
        'productName':v.Product.Product_name,
        'productPrice':v.Product.Product_price,
        'productDescription':v.Product.Product_dis,
    }
    return render_to_pdf('download.html',mydict)


def contact(request):
    return render(request, 'contact.html')


def update_cart_data(request):
    body = json.loads(request.body)
    cart_item= CartItem.objects.get(id=body['cart_id'])
    cart_item.quantity=body['quantity']
    cart_item.save();
    print('id=', body['cart_id'])
    print(body)
    return redirect(cart)


def product_searach(request):
    if request.method=="POST":
        categories=category_details.objects.all()
        value = request.session.get('uname')
        user=User_data.objects.get(username = value)
        search_data = request.POST.get('category')
        if search_data != "0":
            products=product_data.objects.filter(category_id=search_data)
            paginator=Paginator(products, 6)
            page = request.GET.get('page')
            paged_products = paginator.get_page(page)
            product_count = products.count()
        
        context = {
                'categories':categories,
                'user' : user, 
                'product_details' : paged_products,
                'product_count' : product_count,
            }
        return render(request, 'products.html', context)


def wishlist(request, id):
    product_name=product_data.objects.get(id=id)
    check=WishList.objects.filter(user=request.user, Product_id=id)
    if check:
        pass
    else:
        wish=WishList()
        wish.user=request.user
        wish.Product=product_name
        wish.save()
    return redirect(product)


def wish(request):
    if 'uname' in request.session:
        wish_data = WishList.objects.filter(user=request.user)
        context={
            'wish_data':wish_data
        }
        return render(request, 'wishlist.html', context)
    else:
        return redirect(login)


def delete_wish(request, id):
    product_name=product_data.objects.get(id=id)
    check=WishList.objects.filter(user=request.user, Product_id=id)
    check.delete()
    return redirect(wish)

