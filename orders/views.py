from http import client
from time import timezone
from django.shortcuts import render, redirect
from django.contrib import messages
from orders.models import *
from adminside.models import *
from adminside.views import *
from home.views import *
import datetime
import json
import razorpay
from django.utils import timezone


# Create your views here.

def add_new_address(request):
    if 'uname' in request.session:
        u = request.session.get('uname')
        data = User_data.objects.get(username=u)
        if request.method =='POST':
            title=request.POST['title']
            name=request.POST['name']
            email=request.POST['email']
            phone=request.POST['phone']
            pin=request.POST['pin']
            address=request.POST['address']
            city=request.POST['city']
            district=request.POST['district']
            state=request.POST['state']
            country=request.POST['country']
            A=User_data.objects.get(id=data.id)
            if name =='' or email =='' or phone =='' or pin =='' or address =='' or city =='':
                messages.info(request, 'blank space not allowed')
                return redirect(add_new_address)
            else:
                user = Address.objects.create(name = (title and name), user=A, country=country, phone = phone, email = email, state = state, pin =  pin, district=district, full_address=address, city=city)
                user.save(); 
                print('user created')
                return redirect(checkout)
        else:
            context={
                'users_list' : data
                }
            return render(request, 'add_new_address.html', context )
    else:
        return redirect(login)


def delete_address(request, id):
    if 'uname' in request.session:
        user=request.user
        tesin = Address.objects.get(id = id, user = user)
        tesin.delete()
        return redirect(address_list)
    else:
        return redirect(login)


def razor_pay(request):
    print('entering the razorpay block')
    body = json.loads(request.body)
    print(body)
    order = Order.objects.get(user=request.user, is_ordered=False, order_number=body['orderID'])
    payment=Payment(
        user=request.user,
        payment_id=body['payment_id'],
        payment_method="Razorpay",
        amount_paid=order.order_total,
        status="Order Confirmed"
    )
    payment.save()
    
    cart_items = CartItem.objects.filter(user=request.user)
    for item in cart_items:
        print('jithu rao')
        order_product=OrderProduct()
        order_product.order_id=order.id
        order_product.payment=payment
        order_product.user_id=request.user.id
        order_product.Product_id=item.product_id
        order_product.quantity=item.quantity
        order_product.status="Order Placed"
        order_product.product_price=item.product.Product_price
        order_product.ordered=True
        product_details=product_data.objects.get(id=item.product_id)
        product_category=product_details.category_id_id
        order_product.category_id=product_category
        order_product.save()
        

        # reduce the quantity of the sold products
        product = product_data.objects.get(id=item.product_id)
        q=int(product.stoke_status)
        q -= item.quantity
        product.stoke_status=q
        product.save()
        # saving data in coupan applied table
        user = request.user
        apply_coupon = Coupan_applied()
        apply_coupon.user = user
        coupon_id = request.session.get('coupan_session')
        print('id =', coupon_id)
        apply_coupon.coupan= Coupan.objects.get(id=coupon_id)
        apply_coupon.save()

        # deleting coupon session
        if 'coupan_session' in request.session:
            del request.session ['coupan_session']
        # deleting current user cart
        CartItem.objects.filter(user=request.user).delete()
    
    return redirect(cod)


def payments(request):
    body = json.loads(request.body)
    print('body')
    order = Order.objects.get(user=request.user, is_ordered=False, order_number=body['orderID'])

    payment=Payment(
        user=request.user,
        payment_id=body['transID'],
        payment_method=body['payment_method'],
        amount_paid=order.order_total,
        status="Order Confirmed"
    )
    payment.save()

    order.payment=payment
    order.is_ordered=True
    order.save()


    # move the cart items to order product table
    cart_items = CartItem.objects.filter(user=request.user)
    for item in cart_items:
        order_product=OrderProduct()
        order_product.order_id=order.id
        order_product.payment=payment
        order_product.user_id=request.user.id
        order_product.Product_id=item.product_id
        order_product.quantity=item.quantity
        order_product.product_price=item.product.Product_price
        order_product.ordered=True
        product_details=product_data.objects.get(id=item.product_id)
        product_category=product_details.category_id_id
        order_product.category_id=product_category
        order_product.save()
                
        # reduce the quantity of the sold products
        product = product_data.objects.get(id=item.product_id)
        q=int(product.stoke_status)
        q -= item.quantity
        product.stoke_status=q
        product.save()
        # deleting current user cart
        CartItem.objects.filter(user=request.user).delete()
    
    # saving data in coupan applied table
    user = request.user
    apply_coupon = Coupan_applied()
    apply_coupon.user = user
    coupon_id = request.session.get('coupan_session')
    print('id =', coupon_id)
    apply_coupon.coupan= Coupan.objects.get(id=coupon_id)
    apply_coupon.save()
    
    # deleting coupon session
    if 'coupan_session' in request.session:
        del request.session ['coupan_session']

    return render(request, 'cod.html')


def place_order(request, total =0, quantity=0,):
    current_user = request.user
    print(current_user)
    cart_items = CartItem.objects.filter(user=current_user)
   
    cart_count = cart_items.count()
    if cart_count <=0:
        return redirect ('product')

    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        total += (cart_item.product.Product_price * cart_item.quantity)
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
    tax = (1 * discount_price)/100
    grand_total =discount_price+tax
    print(total, grand_total, tax)

    if request.method=="POST":
        address=request.POST['address']
        payment_method=request.POST['payment_method']            

        if address=='' or payment_method=='':
            messages.info(request, 'Enter proper details') 
            return redirect('checkout')
        A=Address.objects.get(id=address)    

        if payment_method == '2':
            data=Order() 
            data.user=current_user
            data.address=A  
            data.payment_method=payment_method
            data.order_total = grand_total 
            data.tax = tax      
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()


            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d") #20210305
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()
        elif payment_method =='3':
            data=Order() 
            data.user=current_user
            data.address=A  
            data.payment_method=payment_method
            data.order_total = grand_total 
            data.tax = tax      
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()


            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d") #20210305
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()
            ruppe = int(grand_total*10)
            order_currency='INR'
            client=razorpay.Client(auth=('rzp_test_Q0RbBFZb49SYt4', '0Maag1tTYVeZHN2jwzVDeIcl'))
            payment=client.order.create({'amount':ruppe, 'currency':order_currency, 'payment_capture':'1'})
            order = Order.objects.get(user=current_user, is_ordered = False, order_number = order_number)
            context ={
                'order':order,
                'cart_items':cart_items,
                'total':total,
                'tax':tax,
                'discount_price':discount_price,
                'discount':discount,
                'grand_total':grand_total,
                'payment_method':payment_method,
                'payment':payment,
            }
            return render(request, 'payment.html', context)
        else:
            data=Order() 
            data.user=current_user
            data.address=A  
            data.is_ordered=True
            data.payment_method=payment_method
            data.order_total = grand_total 
            data.tax = tax      
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()


            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d") #20210305
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()
            CartItem.objects.filter(user=request.user).delete()
            return redirect('cod')

        order = Order.objects.get(user=current_user, is_ordered = False, order_number = order_number)
        context ={
            'order':order,
            'cart_items':cart_items,
            'total':total,
            'discount':discount,
            'discount_price':discount_price,
            'tax':tax,
            'grand_total':grand_total,
            'payment_method':payment_method,
        }
        return render(request, 'payment.html', context)


def cod(request):
    return render(request, 'cod.html')


def apply_coupon(request):
    if request.method=="POST":
        coupan_code = request.POST.get('code')
        c=Coupan.objects.filter(coupan_code=coupan_code)
        if c:
            coupan=Coupan.objects.get(coupan_code=coupan_code)
            d=Coupan_applied.objects.filter(coupan=coupan.id,user=request.user)
            if d:
                messages.info(request,'Already Applied Coupon Code')
                return redirect(checkout)
            now = timezone.now()
            start_date_and_time=coupan.start_date_and_time
            if start_date_and_time < now:
                if now < coupan.end_date_and_time:
                    coupan_id=coupan.id
                    print(coupan_code,coupan_id)
                    request.session['coupan_session']=coupan_id
                    return redirect(checkout)
                else:
                    messages.info(request,'Coupon Expired')
                    return redirect(checkout)
            else:
                messages.info(request,'Coupon is from coupan.start_date_and_time ')
                return redirect(checkout)
        else:
            messages.info(request,'invalid Coupon Code')
            return redirect(checkout)
    return redirect(checkout)







