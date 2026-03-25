from django.shortcuts import render,redirect,get_object_or_404
from . models import signup,user_order,contact
from django.contrib import messages
from admindashboard.models import product

def about(request):
    return render(request,"About.html")

def userinbox(request):
     if "username" in request.session and "emailid" in request.session:
         if request.method=='GET':
             usermail=request.session['emailid']
             data=contact.objects.filter(email=usermail)
             return render(request,"userinbox.html",{"data":data})
         else:
                mesg_id=request.POST.get("message_id")
                usermessage=request.POST.get("usermessage")
                data=contact.objects.get(id=mesg_id)
                data.message=usermessage
                data.save()
                usermail=request.session['emailid']
                data=contact.objects.filter(email=usermail)
                return render(request,"userinbox.html",{"data":data,"message":"Message send Successfully"})
     else:
         messages.error(request,"Please Login Here")
         return render(request,"login.html")
def contacts(request):
    if request.method=='GET':
        return render(request,"contact.html")
    else:
        name=request.POST.get("name")
        email=request.POST.get("email")
        subject=request.POST.get("subject")
        message=request.POST.get("message")
        contact.objects.create(name=name,email=email,subject=subject,message=message)
        return render(request,"contact.html",{"message":name+" Email Send SuccessFully Contact You Asap Thanks."})
def cancelorder(request,id):
    usermail=request.session['emailid']
    product_id=id 
    data=user_order.objects.get(user_emailid=usermail,id=product_id)
    data.order_shipped_status='cancel'
    data.save()
    return redirect("my_order_list")

def myprofile(request):
     if "username" in request.session and "emailid" in request.session:
        usermail=request.session['emailid']
        username=request.session['username']
        data=signup.objects.get(email=usermail)
        return render(request,"profile.html",{"user_info":data,"name":username})
     else:
         messages.error(request,"Please Login Here")
         return render(request,"login.html")
def buynow(request):
     if "username" in request.session and "emailid" in request.session:
        product_id=request.POST.get('pid')
        usermail=request.session['emailid']
        username=request.session['username']
        pqnty=request.POST.get('quantity')
        data=get_object_or_404(product, id=product_id)
        final_price=int(data.pprice)*int(pqnty)
        try:
            user_order.objects.create(user_name=username,user_emailid=usermail,
                                    product_id=product_id,ptype=data.ptype,
                                    pprice=data.pprice,p_photo=data.p_photo.url,
                                    pdescription=data.pdescription,qunatity=pqnty,
                                    total_price=final_price,pname=data.pname)
            return redirect("my_order_list")
        except product.DoesNotExist:
                    messages.error(request,"Product Not Order Tempory out of Service")
                    return render(request,"myorder.html")

     else:
         messages.error(request,"Please Login Here")
         return render(request,"login.html")
     
def my_order_list(request):
    if "username" in request.session and "emailid" in request.session:
        usermail=request.session['emailid']
        username=request.session['username']
        try:
            data=user_order.objects.filter(user_emailid=usermail)
            return render(request,"myorder.html",{"myorder":data,"username":username})
        except user_order.DoesNotExist:
            messages.error(request,"Server Down Please Try Again Later")
            return render(request,"myorder.html")

    else:
         messages.error(request,"Please Login Here")
         return render(request,"login.html")

def product_order(request):
    if "username" in request.session and "emailid" in request.session:
        product_id=request.POST.get('pid')
        data=get_object_or_404(product, id=product_id)
        usermail=request.session['emailid']
        return render(request,"product_order.html",{"products":data,"email":usermail})
    else:
         messages.error(request,"Please Login Here")
         return render(request,"login.html")

def Home_Main_Page(request):
    return render(request,"Home.html")

def create_account(request):
    if request.method=='GET':
        return render(request,"newuser.html")
    else:
        name=request.POST.get("name")
        email=request.POST.get("email")
        mobile=request.POST.get("mobile")
        password=request.POST.get("password")
        photo=request.FILES.get("photo")
        address=request.POST.get("address")
        signup.objects.create(name=name,email=email,mobile=mobile,password=password,photo=photo,address=address)
        return render(request,"newuser.html",{"message":name+" Signup Successfully"})
    

def login(request):
    if request.method=='GET':
        return render(request,"login.html")
    else:
          try:
            email=request.POST.get("email")
            password=request.POST.get("password")
            user=signup.objects.get(email=email,password=password)
            request.session['username']=user.name
            request.session['emailid']=user.email
            return redirect('dashboard')
          except signup.DoesNotExist:
              messages.error(request,"Invalid Email-Id And Password")
              return render(request,"login.html")

def Dashboard(request):
    if "username" in request.session and "emailid" in request.session:
        name=request.session['username']
        data=product.objects.all()
        return render(request,"Dashboard.html",{"username":name,"product":data})
    else:
         messages.error(request,"Please Login Here")
         return render(request,"login.html")
def Logout(request):
    request.session.clear()
    messages.error(request,"Logout Successfully")
    return render(request,"login.html")

def change_password(request):
     if "username" in request.session and "emailid" in request.session:
        if request.method=='GET':
             usermail=request.session['emailid']
             return render(request,"changepassword.html",{"email":usermail})
        else:
            usermail=request.session['emailid']
            oldpassword=request.POST.get("oldpassword")
            newpassword=request.POST.get("newpassword")
            confirmpassword=request.POST.get("confirmpassword")
            try:
                user=signup.objects.get(email=usermail,password=oldpassword)
                if newpassword==confirmpassword:
                    user.password=newpassword
                    user.save()
                    messages.error(request,"Password Change Successfully")
                    return render(request,"changepassword.html",{"email":usermail})
                else:
                    messages.error(request,"Confirm And New Password MisMatch")
                    return render(request,"changepassword.html",{"email":usermail})
            except signup.DoesNotExist:
              messages.error(request,"Invalid Old Password")
              return render(request,"changepassword.html",{"email":usermail})

     else:
         messages.error(request,"Please Login Here")
         return render(request,"login.html")

