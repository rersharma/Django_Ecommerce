from django.shortcuts import render,redirect,get_object_or_404
from . models import admin_user,product
from django.contrib import messages
from userdashboard.models import user_order,contact
from django.db.models import Count
from django.db.models.functions import ExtractMonth
import json


def admininbox(request):
        if "admin_email" in request.session:
         if request.method=='GET':
                record=contact.objects.all()
                print("value is ",record)
                return render(request,"inbox.html",{"data":record})
         else:
                mesg_id=request.POST.get("message_id")
                adminmessage=request.POST.get("adminmessage")
                data=contact.objects.get(id=mesg_id)
                data.reply=adminmessage
                data.save();
                record=contact.objects.all()
                print("value is ",record)
                return render(request,"inbox.html",{"data":record,"message":"Reply Send Successfully"})
        else:
             return render(request,"admin_login.html")


def manage_product(request):
    if "admin_email" in request.session:
        record=product.objects.all()
        return render(request,"manage_product.html",{"data":record})
    else:
        return render(request,"admin_login.html")

def product_delete(request,id):
    if "admin_email" in request.session:
        pr=get_object_or_404(product,id=id)
        pr.delete()
        return redirect('manage_product')
    else:
        return render(request,"admin_login.html")
def product_add(request):
     if "admin_email" in request.session:
        if request.method=='GET':
            return render(request,'add_product.html')
        else:
            name=request.POST.get("name")
            ptype=request.POST.get("ptype")
            price=request.POST.get("price")
            photo=request.FILES.get("photo")
            descrption=request.POST.get("description")
            product.objects.create(pname=name,ptype=ptype,pprice=price,p_photo=photo,pdescription=descrption)
            messages.success(request,name+" Product Added Successfully")
            return render(request,"add_product.html")     
     else:
        return render(request,"admin_login.html")
     
def userorder(request):
    if "admin_email" in request.session:
        data=user_order.objects.all() 
        return render(request,"userorderlist.html",{"userorders":data})
    else:
        return render(request,"admin_login.html")

def remark_order(request):
    if "admin_email" in request.session:
        orderid=request.POST.get('orderid')
        remark=request.POST.get('remark')
        getinfo=user_order.objects.get(id=orderid)
        getinfo. order_shipped_status=remark
        getinfo.save()
        return redirect('userorder')
    else:
        return render(request,"admin_login.html")


def check_user(request):
    if request.method=='GET':
        return render(request,"admin_login.html")
    else:
        email=request.POST.get("email")
        password=request.POST.get("password")
        try:
            admin_usr=admin_user.objects.get(email=email,password=password)
            request.session['admin_email']=email
            return redirect("admin_dashboard")
        except admin_user.DoesNotExist:
              messages.error(request,"Invalid Email-Id And Password")
              return render(request,"admin_login.html")

def admin_dash(request):
    if "admin_email" in request.session:
          # Step 1: Get count grouped by month
        data = (
            user_order.objects
            .annotate(month=ExtractMonth('order_date'))
            .values('month')
            .annotate(total=Count('id'))
            .order_by('month')
        )

        # Step 2: Initialize all months with 0
        monthly_orders = [0] * 12  # Jan to Dec

        # Step 3: Fill actual data
        for item in data:
            month_index = item['month'] - 1  # Convert 1–12 → 0–11
            monthly_orders[month_index] = item['total']
        cancel_by_admdin_count=user_order.objects.filter(order_shipped_status='Cancel By Admin')
        Packed_count=user_order.objects.filter(order_shipped_status='Packed')
        Confirmed_count=user_order.objects.filter(order_shipped_status='Confirmed')
        Shipped_count=user_order.objects.filter(order_shipped_status='Shipped')
        user_cancel_count=user_order.objects.filter(order_shipped_status='cancel')
        Delivered_count=user_order.objects.filter(order_shipped_status='Delivered')

        electronic_count=product.objects.filter(ptype="Electronic")
        cloth_count=product.objects.filter(ptype="Cloth")
        Grocery_count=product.objects.filter(ptype="Grocery")
        Furniture_count=product.objects.filter(ptype="Furniture")
        context = {
                            "monthly_orders": json.dumps(monthly_orders),  # convert to JS format
                            "c_a":len(cancel_by_admdin_count),
                            'c_ct':len(Confirmed_count),
                            'p_c':len(Packed_count),
                            'sh_ct':len(Shipped_count),
                            'ur_cancel':len(user_cancel_count),
                            'Dl_c':len(Delivered_count),
                            'electronic_count':len(electronic_count),
                            'cloth_count':len(cloth_count),
                            'Grocery_count':len(Grocery_count),
                            'Furniture_count':len(Furniture_count)
                 }
        

            
      

        return render(request,"admin_dashboard.html",context)
    else:
        messages.error(request,"Please Login Here")
        return render(request,"admin_login.html")



def Logout(request):
    request.session.clear()
    messages.error(request,"Logout Successfully")
    return render(request,"admin_login.html")