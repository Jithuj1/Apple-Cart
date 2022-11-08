from ast import Pass
import datetime
import csv
import re
from urllib import request
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate
from home.models import *
from home.views import *
from orders.models import *
from adminside.models import *
from django.core.paginator import *
from adminside.models import SalesReport
from django.db.models import Sum
from django.http import HttpResponse
import xlwt
from xhtml2pdf import pisa
from django.template.loader import *


# Create your views here.

def admin_home(request):
    if 'username' in request.session:
        today=0
        count=0
        total=0
        stock=0
        total_sale = OrderProduct.objects.all()
        for i in total_sale:
            total+=i.product_price
            count+=1
        today_sale =OrderProduct.objects.filter(updated_at=datetime.date.today().strftime("%Y-%m-%d"))
        for i in today_sale:
            today+=i.product_price
        total_stock=product_data.objects.all()
        data_sales = []
        for i in total_stock:
            stock+=int(i.stoke_status)
            data = OrderProduct.objects.filter(Product_id=i.id).count()
            data_sales.append(data)
        print(data_sales)
        context={
            'total':total,
            'today':today,
            'stock':stock,
            'count':count,
            'data_sales':data_sales,
            'total_stock':total_stock,
        }
        return render (request, 'adminhome.html', context)
    else:
        return redirect (admin_login)


def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(username, password)
        check = authenticate(username= username, password = password)
        print('check',check)
        if check is not None:
            value = User_data.objects.filter(username=username)
            for i in value:
                if i.is_superadmin is True:
                    request.session['username'] = username
                    return redirect('admin_home')
                else:
                    messages.error(request, "Only for admin")
                    return redirect('admin_login')
        else:
            messages.error(request, "incorrect password or username")
            return redirect('admin_login')
    else:
        return render (request, 'adminlogin.html')


def admin_logout(request):
    if 'username' in request.session:
        del request.session['username']
        return redirect(admin_login)
    
    
def users(request):
    if 'username' in request.session:
        if request.method == 'POST':
            search_data = request.POST.get('search')
            print('search', search_data )
            if len(search_data) == 0:
                a = User_data.objects.all()
                return render(request, 'users.html', {'data':a})
            data_view = User_data.objects.filter(name__icontains=search_data)
            paginator=Paginator(data_view, 20)
            page = request.GET.get('page')
            paged_products = paginator.get_page(page)
            return render(request,'users.html',{'data':paged_products})
        else:
            a = User_data.objects.all()
            paginator=Paginator(a, 20)
            page = request.GET.get('page')
            paged_products = paginator.get_page(page)
            return render(request, 'users.html', {'data':paged_products})    
    else:
        return redirect('admin_login')
    

def block(request, id):
    if 'username' in request.session:
        data = User_data.objects.get(id=id)
        print('id', id)
        data.status = False
        data.save()
        return redirect(users)
    else:
        return redirect('admin_login')


def unblock(request, id):
    if 'username' in request.session:
        data = User_data.objects.get(id=id)
        data.status = True
        data.save()
        return redirect(users)
    else:
        return redirect('admin_login')


def product_list(request):
    if 'username' in request.session:
        if request.method =='POST':
            search_data=request.POST.get('search')
            if len(search_data)=='':
                a=product_data.objects.all()
                paginator=Paginator(a, 20)
                page = request.GET.get('page')
                paged_products = paginator.get_page(page)
                return render (request, 'productlist.html', {'data':paged_products})
            else:
                a = product_data.objects.filter(Product_name__icontains = search_data)
                paginator=Paginator(a, 20)
                page = request.GET.get('page')
                paged_products = paginator.get_page(page)
                return render (request, 'productlist.html', {'data':paged_products})
        else:
            a=product_data.objects.all()
            paginator=Paginator(a, 20)
            page = request.GET.get('page')
            paged_products = paginator.get_page(page)
            return render (request,'productlist.html', {'data':paged_products})
    else:
        return redirect(admin_login)


def add_new_product(request):
    if 'username' in request.session:
        if request.method == 'POST':
            id= request.POST.get('p_id')
            name= request.POST.get('p_name')
            dis= request.POST.get('p_dis')
            price= request.POST.get('price')
            ram= request.POST.get('ram')
            storage= request.POST.get('storage')
            category= request.POST.get('category')
            img1= request.FILES.get('file1')
            img2= request.FILES.get('file2')
            img3= request.FILES.get('file3')
            img4= request.FILES.get('file4')
            A=category_details.objects.get(id=category)
            if id == '' or name =='' or dis == ''or price == '' or ram == '' or storage == '' or img1 == '' or img2 == '' or img3 == '' or img4 == '':
                messages.error(request, 'blank space not allowed')
                return redirect(add_new_product)
            else:
                product = product_data.objects.create(product_ID = id, Product_name=name, Product_dis=dis, Product_price=price, ram=ram, storage=storage, type=category, image1 =img1, image2 =img2, image3 = img3, image4 = img4, category_id=A)
                product.save()
                return redirect(product_list)
        else:
            a=category_details.objects.all
            return render(request, 'addnewproduct.html', {'data':a})
    else:
        return redirect(admin_login)       
        

def update_product(request,id):
    if 'username' in request.session:
        if request.method == 'POST':
            a = product_data.objects.get (id = id )
            a.Product_name= request.POST.get('p_name')
            a.Product_dis= request.POST.get('p_dis')
            a.Product_price= request.POST.get('price')
            a.ram= request.POST.get('ram')
            a.storage= request.POST.get('storage')
            a.image1= request.FILES.get('file1')
            a.image2= request.FILES.get('file2')
            a.image3= request.FILES.get('file3')
            a.image4= request.FILES.get('file4')
            a.save(); 
            messages.info(request, 'category updated')
            return redirect(product_list)
        else:
            a = product_data.objects.get(id = id )
            return render (request, 'update_product.html', {'data':a})    

    else:
        return redirect(admin_login)


def delete_product(request, id):
    a = product_data.objects.get(id = id)
    a.delete();
    return redirect(product_list)
        

def add_new_category(request):
    if 'username' in request.session:
        if request.method == 'POST':
            id= request.POST.get('c_id')
            name= request.POST.get('c_name')
            dis= request.POST.get('c_dis')
            img= request.FILES.get('c_image')
            if category_details.objects.filter(category_id=id).exists():
                messages.info(request, 'id already taken')
                return redirect(add_new_category)
            else:
                user = category_details.objects.create(category_id = id, category_name = name, category_dis = dis, img=img)
                user.save(); 
                messages.info(request, 'user created')
                return redirect(category)

        return render(request, 'addnewcategory.html')
    else:       
        return redirect(admin_login)


def update_category(request, id):
    if 'username' in request.session:
        if request.method == 'POST':
            a = category_details.objects.get(id=id)  
            a.category_name = request.POST.get('c_name')
            a.category_dis= request.POST.get('c_dis')
            a.img= request.FILES.get('c_image')
            a.save(); 
            messages.info(request, 'category updated')
            return redirect(category)
        else:
            a = category_details.objects.get(id=id)       
            return render(request, 'update_category.html', {'data1':a})
    else:
        return redirect(admin_login)


def delete_category(request, id):
    a = category_details.objects.get(id = id)
    a.delete()
    return redirect(category)
    

def category(request):
    if 'username' in request.session:
        a = category_details.objects.all()
        paginator=Paginator(a, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        return render (request,'category.html', {'data':paged_products})
    else:
        return redirect(admin_login)
    

def address_list(request):
    if 'uname' in request.session:
        user=request.user
        list= Address.objects.filter(user=user)
        context={
            'list':list
        }
        return render(request, 'address_list.html', context)
    else:
        return redirect(login)


def order_list(request):
    if 'username' in request.session:
        if request.method=="POST":
            search_value = request.POST.get('search')
            if search_value =="":
                order = OrderProduct.objects.all()
                paginator=Paginator(order, 12)
                page = request.GET.get('page')
                paged_products = paginator.get_page(page)
                return render(request, 'order_list.html', {'data':paged_products}) 
            try:
                d = Order.objects.get(order_number=search_value)
                if d:
                    order = OrderProduct.objects.filter(order_id=d.id)
                    paginator=Paginator(order, 12)
                    page = request.GET.get('page')
                    paged_products = paginator.get_page(page)
                    return render(request, 'order_list.html', {'data':paged_products})
                else:
                    return render(request, 'order_list.html')
            except:
                return render(request, 'order_list.html')
        else:
            order = OrderProduct.objects.all()
            paginator=Paginator(order, 12)
            page = request.GET.get('page')
            paged_products = paginator.get_page(page)
            return render(request, 'order_list.html', {'data':paged_products})
    else:
        return redirect(admin_login)


def update_order(requset, id):
    order = OrderProduct.objects.get(id=id)
    context={
        'order':order,
    }
    return render(requset, 'update_order.html', context)


def submit_order(request, id):
    if 'username' in request.session:
        data = OrderProduct.objects.get(id=id)
        if request.method == "POST":
            value  = request.POST['status']
            print(value)
            data.status = value
            data.save()
        return redirect(order_list)
    else:
        return redirect(admin_login)


def sales(request):
    if 'username' in request.session:
        if request.method =="POST":
            if request.POST.get('month'):
                month = request.POST.get('month')
                data=OrderProduct.objects.filter(created_at__icontains = month)
                if data:
                    if SalesReport.objects.all():
                        SalesReport.objects.all().delete()
                        for i in data:
                            sales = SalesReport()
                            sales.productName=i.Product.Product_name
                            sales.categoryName=i.category.category_name
                            sales.date=i.created_at
                            sales.quantity=i.quantity
                            sales.productPrice=i.product_price
                            sales.save()
                        sales = SalesReport.objects.all()
                        total= SalesReport.objects.all().aggregate(Sum('productPrice'))

                        paginator=Paginator(sales, 12)
                        page = request.GET.get('page')
                        paged_products = paginator.get_page(page)
                        context = {
                            'sales': paged_products,
                            'total' : total['productPrice__sum']
                        }
                        print(total, "jithu")
                        return render(request, 'sales.html', context)
                    else:
                        for i in data:
                            sales = SalesReport()
                            sales.productName=i.Product.Product_name
                            sales.categoryName=i.category.category_name
                            sales.date=i.created_at
                            sales.quantity=i.quantity
                            sales.productPrice=i.product_price
                            sales.save()
                        sales = SalesReport.objects.all()
                        total= SalesReport.objects.all().aggregate(Sum('productPrice'))
                        paginator=Paginator(sales, 6)
                        page = request.GET.get('page')
                        paged_products = paginator.get_page(page)
                        context = {
                            'sales': paged_products,
                            'total' : total['productPrice__sum']
                        }
                        return render(request, 'sales.html', context)
                else:
                    SalesReport.objects.all().delete()
                    return render(request, 'sales.html')
            elif request.POST.get('date'):
                date = request.POST.get('date')
                data=OrderProduct.objects.filter(created_at__icontains = date)
                if data:
                    if SalesReport.objects.all():
                        SalesReport.objects.all().delete()
                        for i in data:
                            sales = SalesReport()
                            sales.productName=i.Product.Product_name
                            sales.categoryName=i.category.category_name
                            sales.date=i.created_at
                            sales.quantity=i.quantity
                            sales.productPrice=i.product_price
                            sales.save()
                        sales = SalesReport.objects.all()
                        total= SalesReport.objects.all().aggregate(Sum('productPrice'))

                        paginator=Paginator(sales, 12)
                        page = request.GET.get('page')
                        paged_products = paginator.get_page(page)
                        context = {
                            'sales': paged_products,
                            'total' : total['productPrice__sum']
                        }
                        return render(request, 'sales.html', context)
                    else:
                        for i in data:
                            sales = SalesReport()
                            sales.productName=i.Product.Product_name
                            sales.categoryName=i.category.category_name
                            sales.date=i.created_at
                            sales.quantity=i.quantity
                            sales.productPrice=i.product_price
                            sales.save()
                        sales = SalesReport.objects.all()
                        total = SalesReport.objects.all().aggregate(Sum('productPrice'))
                        paginator=Paginator(sales, 12)
                        page = request.GET.get('page')
                        paged_products = paginator.get_page(page)
                        context = {
                            'sales': paged_products,
                            'total' : total['productPrice__sum']
                        }
                        return render (request, 'sales.html', context)
                else:
                    SalesReport.objects.all().delete()
                    return render(request, 'sales.html')
            elif request.POST.get('date1'):
                date1 = request.POST.get('date1')
                date2 = request.POST.get('date2')
                data=OrderProduct.objects.filter(created_at__range=(date1, date2))
                if data:
                    if SalesReport.objects.all():
                        SalesReport.objects.all().delete()
                        for i in data:
                            sales = SalesReport()
                            sales.productName=i.Product.Product_name
                            sales.categoryName=i.category.category_name
                            sales.date=i.created_at
                            sales.quantity=i.quantity
                            sales.productPrice=i.product_price
                            sales.save()
                        sales = SalesReport.objects.all()
                        total= SalesReport.objects.all().aggregate(Sum('productPrice'))
                        paginator=Paginator(sales, 12)
                        page = request.GET.get('page')
                        paged_products = paginator.get_page(page)
                        context = {
                            'sales': paged_products,
                            'total' : total['productPrice__sum']
                        }
                        return render(request, 'sales.html', context)
                    else:
                        for i in data:
                            sales = SalesReport()
                            sales.productName=i.Product.Product_name
                            sales.categoryName=i.category.category_name
                            sales.date=i.created_at
                            sales.quantity=i.quantity
                            sales.productPrice=i.product_price
                            sales.save()
                        sales = SalesReport.objects.all()
                        total = SalesReport.objects.all().aggregate(Sum('productPrice'))
                        paginator=Paginator(sales, 12)
                        page = request.GET.get('page')
                        paged_products = paginator.get_page(page)
                        context = {
                            'sales': paged_products,
                            'total' : total['productPrice__sum']
                        }
                    return render(request, 'sales.html')
            else:
                year = request.POST.get('year')
                data=OrderProduct.objects.filter(created_at__icontains = year)
                if data:
                    if SalesReport.objects.all():
                        SalesReport.objects.all().delete()
                        for i in data:
                            sales = SalesReport()
                            sales.productName=i.Product.Product_name
                            sales.categoryName=i.category.category_name
                            sales.date=i.created_at
                            sales.quantity=i.quantity
                            sales.productPrice=i.product_price
                            sales.save()
                        sales = SalesReport.objects.all()
                        total= SalesReport.objects.all().aggregate(Sum('productPrice'))
                        paginator=Paginator(sales, 12)
                        page = request.GET.get('page')
                        paged_products = paginator.get_page(page)
                        context ={
                            'sales':paged_products,
                            'total':total['productPrice__sum']
                            
                        }
                        return render(request, 'sales.html', context)
                    else:
                        for i in data:
                            sales = SalesReport()
                            sales.productName=i.Product.Product_name
                            sales.categoryName=i.category.category_name
                            sales.date=i.created_at
                            sales.quantity=i.quantity
                            sales.productPrice=i.product_price
                            sales.save()
                        sales = SalesReport.objects.all()
                        total = SalesReport.objects.all().aggregate(Sum('productPrice'))
                        paginator=Paginator(sales, 12)
                        page = request.GET.get('page')
                        paged_products = paginator.get_page(page)
                        context = {
                            'sales': paged_products,
                            'total' : total['productPrice__sum']
                        }
                        return render (request, 'sales.html', context)
                else:
                    SalesReport.objects.all().delete()
                    return render(request, 'sales.html')      
        else:
            data=OrderProduct.objects.all()
            if data:
                if SalesReport.objects.all():
                    SalesReport.objects.all().delete()
                for i in data:
                    sales = SalesReport()
                    sales.productName=i.Product.Product_name
                    sales.categoryName=i.category.category_name
                    sales.date=i.created_at
                    sales.quantity=i.quantity
                    sales.productPrice=i.product_price
                    sales.save()
                sales = SalesReport.objects.all()
                total = SalesReport.objects.all().aggregate(Sum('productPrice'))
                paginator=Paginator(sales, 12)
                page = request.GET.get('page')
                paged_products = paginator.get_page(page)
                context = {
                    'sales': paged_products,
                    'total': total['productPrice__sum'],
                }
                return render(request, 'sales.html', context)
            else:
                return render(request, 'sales.html')
    else:
        return redirect(admin_login)


def export_to_excel(request):
    response = HttpResponse(content_type = 'application/ms-excel')
    response['content-Disposition'] = 'attachment; filename="sales.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Sales Report') #this will generate a file named as sales Report

     # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Product Name','Category','Price','Quantity', ]

    for col_num in range(len(columns)):
        # at 0 row 0 column
        ws.write(row_num, col_num, columns[col_num], font_style)

    
    font_style = xlwt.XFStyle()
    total = 0

    rows = SalesReport.objects.values_list(
        'productName','categoryName', 'productPrice', 'quantity')
    for row in rows:
        total +=row[2]
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
    row_num += 1
    col_num +=1
    ws.write(row_num,col_num,total,font_style)

    wb.save(response)

    return response


def export_to_pdf(request):
    prod = product_data.objects.all()
    order_count = []
    # for i in prod:
    #     count = SalesReport.objects.filter(product_id=i.id).count()
    #     order_count.append(count)
    #     total_sales = i.price*count
    sales = SalesReport.objects.all()
    total_sales = SalesReport.objects.all().aggregate(Sum('productPrice'))



    template_path = 'sales_pdf.html'
    context = {
        'brand_name':prod,
        'order_count':sales,
        'total_amount':total_sales['productPrice__sum'],
    }
    
    # csv file can also be generated using content_type='application/csv
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'

    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')

    return response


def export_to_csv(request):
    response = HttpResponse(content_type ='text/csv')
    writer = csv.writer(response)
    writer.writerow(['Product Name', 'Date', 'Quantity', 'Product Price'])
    for member in OrderProduct.objects.all().values_list('product_name', 'created_at', 'quantity', 'product_price'):
        writer.writerow(member)
    response['content-disposition']= 'attachment; filename ="data.csv"'
    return response


def offer_page(request):
    if 'username' in request.session:
        return render(request, 'offers.html')
    else:
        return redirect(admin_login)


def add_new_coupon(request):
    if 'username' in request.session:
        if request.method == "POST":
            name = request.POST.get('coupon_name')
            date1 = request.POST.get('date1')
            date2 = request.POST.get('date2')
            percentage = request.POST.get('dis_percentage')
            coupon = Coupan () 
            coupon.coupan_code = name
            coupon.start_date_and_time = date1
            coupon.end_date_and_time = date2
            coupon.discount_percentage = percentage
            coupon.save()
            return redirect(coupon_page)
        else:
            return render(request, 'add_new_coupon.html')
    else:
        return redirect(admin_login)


def coupon_page(request):
    if 'username' in request.session:
        coupens = Coupan.objects.all()
        context ={
            'coupens':coupens
        }
        return render(request, 'coupen_page.html', context)
    else:
        return redirect(admin_login)


def category_offer_page(request):
    if 'username' in request.session:
        category = CategoryOffer.objects.all()
        context ={
            'category':category
        }
        return render(request, 'category_offer_page.html', context)
    else:
        return redirect(admin_login)


def add_category_offer(request):
    if 'username' in request.session:
        category = category_details.objects.all()
        context ={
            'category':category
        }
        if request.method == "POST":
            name = request.POST.get('name')
            category_id = request.POST.get('c_id')
            start_date = request.POST.get('date1')
            end_date = request.POST.get('date2')
            dis_persentage = request.POST.get('dis_percentage')
            if name == '' or category_id == '' or end_date == '' or dis_persentage == '':
                messages.error(request, "Blank Space is not available")
                return redirect('add_category_offer')
            categoryoff = CategoryOffer()
            categoryoff.Name=name
            categoryoff.cid=category_details.objects.get(id=category_id)
            categoryoff.valid_till=end_date
            categoryoff.percentage=dis_persentage
            categoryoff.save()
            return redirect(category_offer_page)

        return render(request, 'add_category_offer.html', context)
    else:
        return redirect(admin_login)


def product_offer_page(request):
    if 'username' in request.session:
        product = ProductOffer.objects.all()
        context ={
            'product':product
        }
        return render(request, 'product_offer_page.html', context)
    else:
        return redirect(admin_login)


def add_product_offer(request):
    if 'username' in request.session:
        product = product_data.objects.all()
        context ={
            'product':product
        }
        if request.method == "POST":
            name = request.POST.get('name')
            product_id = request.POST.get('p_id')
            print(product_id)
            start_date = request.POST.get('date1')
            end_date = request.POST.get('date2')
            dis_persentage = request.POST.get('dis_percentage')
            if name == '' or product_id == '' or end_date == '' or dis_persentage == '':
                messages.error(request, "Blank Space is not available")
                return redirect('add_category_offer')
            productoff = ProductOffer()
            productoff.Name=name
            productoff.pid=product_data.objects.get(id=product_id)
            productoff.valid_till=end_date
            productoff.percentage=dis_persentage
            productoff.save()
            return redirect(product_offer_page)
        return render(request, 'add_product_offer.html', context)
    else:
        return redirect(admin_login)


def delete_product_offer(request, id):
    offer_data = ProductOffer.objects.get(id = id)
    product = product_data.objects.get(id = offer_data.pid_id)
    product.discount_price = product.Product_price
    product.save()
    offer_data.delete()
    return redirect(product_offer_page)


def delete_category_offer(request, id):
    offer_data = CategoryOffer.objects.get(id = id)
    product = product_data.objects.filter(id = offer_data.cid_id)
    for i in product:
        i.discount_price = i.Product_price
        i.save()
    offer_data.delete()
    return redirect(category_offer_page)


def delete_coupon(request, id):
    coupon = Coupan.objects.get(id=id)
    coupon.delete()
    return redirect(coupon_page)