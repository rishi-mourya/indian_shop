from django.shortcuts import render, redirect
from mainApp.models import *
from django.contrib import messages
# This module for import User from admin page and create new user also with buyers
from django.contrib.auth.models import User
# This is for import ready login and logout sessions,....authenticate for redirect admin page with admin login
from django.contrib.auth import login, logout, authenticate
# if you use this module you don't need a again again login or logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q #this library for searching ////like query

from random import randrange#this is for generate OTP numbers

from django.conf import settings#email procedure
from django.core.mail import send_mail# from google for email


#these are for razor/online payment
from indian_shop.settings import RAZORPAY_API_KEY,RAZORPAY_API_SECRET_KEY#our file name and settings file
import razorpay




def home(Request):  # 1 step
    # order_by for after added products show in front firstly through ID and using reverse method for reverse id like decending
    data = Product.objects.all().order_by('id').reverse()[:8]
    # [:8] it is only for showing 8 lattest Product on Home Page
    return render(Request, 'index.html', {'data': data})


def shopPage(Request, mc, sc, br):  # 2 step
     # now we are filtering our products
    if (mc == 'All' and sc == 'All' and br == 'All'):
        data = Product.objects.all().order_by('id').reverse()
    elif (mc != 'All' and sc == 'All' and br == 'All'):
        data = Product.objects.filter(
            maincategory=Maincategory.objects.get(name=mc)).order_by('id').reverse()
    elif (mc == 'All' and sc != 'All' and br == 'All'):
        data = Product.objects.filter(
            subcategory=Subcategory.objects.get(name=sc)).order_by('id').reverse()
    elif (mc == 'All' and sc == 'All' and br != 'All'):
        data = Product.objects.filter(
            brand=Brand.objects.get(name=br)).order_by('id').reverse()
    elif (mc != 'All' and sc != 'All' and br == 'All'):
        data = Product.objects.filter(maincategory=Maincategory.objects.get(
            name=mc), subcategory=Subcategory.objects.get(name=sc)).order_by('id').reverse()
    elif (mc != 'All' and sc != 'All' and br == 'All'):
        data = Product.objects.filter(maincategory=Maincategory.objects.get(
            name=mc), subcategory=Subcategory.objects.get(name=sc)).order_by('id').reverse()
    elif (mc != 'All' and sc == 'All' and br != 'All'):
        data = Product.objects.filter(maincategory=Maincategory.objects.get(
            name=mc), brand=Brand.objects.get(name=br)).order_by('id').reverse()
    elif (mc == 'All' and sc != 'All' and br != 'All'):
        data = Product.objects.filter(brand=Brand.objects.get(
            name=br), subcategory=Subcategory.objects.get(name=sc)).order_by('id').reverse()
    else:
         data = Product.objects.filter(maincategory=Maincategory.objects.get(name=mc), brand=Brand.objects.get(
             name=br), subcategory=Subcategory.objects.get(name=sc)).order_by('id').reverse()
    maincategory = Maincategory.objects.all()
    subcategory = Subcategory.objects.all()
    brand = Brand.objects.all()

    return render(Request, 'shop.html', {'data': data, 'maincategory': maincategory, 'subcategory': subcategory, 'brand': brand, 'mc': mc, 'sc': sc, 'br': br})


def singleProduct(Request, id):  # 3 step
    data = Product.objects.get(id=id)
    return render(Request, 'single-product.html', {'data': data})


def loginPage(Request):  # 5 step
    if (Request.method == "POST"):
        username = Request.POST.get('username')
        password = Request.POST.get('password')
        # check user object
        user = authenticate(username=username, password=password)
        if (user is not None):  # if user available so it will give us NOT None
            login(Request, user)
            if (user.is_superuser):
                return redirect("/admin/")
            else:
                return redirect("/profile/")
        else:  # if user is not available so it will give us "None"
            messages.error(Request, 'Invalid Username or Password!!!')

    return render(Request, 'login.html')


def logoutPage(Request):  # 6 step
    logout(Request)
    return redirect('/login/')


def signupPage(Request):  # 4 step
    if (Request.method == 'POST'):
        p = Request.POST.get('password')
        cp = Request.POST.get('cpassword')
        phone= Request.POST.get('phone')
        
        if (phone>='0' and phone<='9') and (len(phone)>=7):#phone number must be Numbers not alphabet and length of number must be greater 7

            if p == cp:  # check password and confirm password is correct or not
                if len(p)>=8:
                    b = Buyer()
                    b.name = Request.POST.get('name')
                    b.username = Request.POST.get('username')
                    b.email = Request.POST.get('email')
                    b.phone = phone
                    user = User(username=b.username, email=b.email)  # User Already in library
                    if user:  # check username is taken or not
                        user.set_password(p)#after username and email/set password keyword
                        user.save()  # we are creating 2 accounts USER and BUYER
                        b.save()  # Buyer details is saving
                       
                        #for email 
                        subject = f'{b.name}, Your Account is Created : Team Indian_shop'
                        message = f'Thank You to Create Your Account With us, Now You Can Buy Our Lattest Products : Team Indian_shop'# sending email for inform signup successfully
                        email_from = settings.EMAIL_HOST_USER
                        recipient_list = [b.email,]# whom do you want to send email ? "b.email" because b is Buyer
                        send_mail( subject, message, email_from, recipient_list )#No change
                        return redirect('/login/')
                    
                    else:  # if username is already taken on signup time!!
                        messages.error(Request, "Username is already taken!!!")
                        
                else:#if password length is not greater than 8
                    messages.error(Request, "Password length must be greater than 8 and with the help of @/123!!!")
            else:
                messages.error(Request, "Your Password and Confirm Passwrod doesn't match!!!")
        else:#if phone number is not integer or less than 7 length
            messages.error(Request, "Phone number must be Integer or Phone number less than Seven will not be taken!!!")
    return render(Request, 'signup.html')


# before getting profile page, it will check that loggin or not if you didn't login so,it will redirect login page
@login_required(login_url='/login/')
def profilePage(Request):  # 7 step
    # check user table that user available or not
    user = User.objects.get(username=Request.user)

    # check login candidate is admin or not,if user is admin so we will redirect(adminpanel)
    if user.is_superuser:
        return redirect('/admin/')
    else:
        # check buyer table that user is or not
        buyer = Buyer.objects.get(username=user.username)
        # we are filtering wishlist products
        wishlist = Wishlist.objects.filter(user=buyer)#we are taking after creating wishlist
        orders= Checkout.objects.filter(user=buyer)#we are taking after set OrderPage
    return render(Request, 'profile.html', {'user': buyer, 'wishlist': wishlist,'orders':orders})


@login_required(login_url='/login/')
def updatePage(Request):  # 8 step
    # check user table that user available or not
    user = User.objects.get(username=Request.user)
    # check login candidate is admin or not,if user is admin so we will redirect(adminpanel)
    if user.is_superuser:
        return redirect('/admin/')
    else:
        # check buyer table that user is or not
        buyer = Buyer.objects.get(username=user.username)
        if (Request.method == "POST"):
            buyer.name = Request.POST.get("name")
            buyer.email = Request.POST.get("email")
            buyer.phone = Request.POST.get("phone")
            buyer.addressline1 = Request.POST.get("addressline1")
            buyer.addressline2 = Request.POST.get("addressline2")
            buyer.addressline3 = Request.POST.get("addressline3")
            buyer.pin = Request.POST.get("pin")
            buyer.city = Request.POST.get("city")
            buyer.state = Request.POST.get("state")
            if (Request.FILES.get("pic")):  # if you go to upload on option and click, and without upload image you click on update page without upload image so image will be old pic
                # when we take a data of pic and file so we are used "Request.FILES.get()"
                buyer.pic = Request.FILES.get("pic")
            buyer.save()
            return redirect("/profile")
    return render(Request, 'update-profile.html', {'user': buyer})


@login_required(login_url='/login/')
def addToCart(Request, id):  # 9 step
    # Request.session.flush() #it is work delete session of recent added items
    # whetever you get a details of cart, details will get you securely through server not browser
    cart = Request.session.get('cart', None)
    p = Product.objects.get(id=id)
    if (cart is None):  # if cart already not exists..means empty cart
        cart = {str(p.id): {'pid': p.id, 'pic': p.pic1.url, 'name': p.name, 'color': p.color, 'size': p.size, 'price': p.finalprice,
                    'qty': 1, 'total': p.finalprice, 'maincategory': p.maincategory.name, 'subcategory': p.subcategory.name, 'brand': p.brand.name}}
        # we are using maincategory.name because we want name and foreign key exists so we can't find maincategory
    else:  # if cart is not empty,
        if (str(p.id) in cart):  # if product.id in cart already so
            item = cart[str(p.id)]
            item['qty'] = +1  # we are adding quantity of product +1
            item['total'] = item['total']+item['price']
            cart[str(p.id)] = item
        else:
            # setdefault takes 2 argument (key,values) with help of comma(,)
            cart.setdefault(str(p.id), {'pid': p.id, 'pic': p.pic1.url, 'name': p.name, 'color': p.color, 'size': p.size, 'price': p.finalprice,
                            'qty': 1, 'total': p.finalprice, 'maincategory': p.maincategory.name, 'subcategory': p.subcategory.name, 'brand': p.brand.name})
            # if cart empty so we will add product through dict and dict keyword (setdefault) for add something in dict

    Request.session['cart'] = cart
    # timing for added product expiry life
    Request.session.set_expiry(60*60*24*30)
    return redirect('/cart')  # it will call cartPage


@login_required(login_url='/login/')
def cartPage(Request):  # 10 step and depend on add to cart page
    cart = Request.session.get('cart', None)
    c = []  # empty array or list
    total = 0
    shipping = 0
    if (cart is not None):
        for value in cart.values():
            # add old product price and new product price
            total = total + value['total']
            c.append(value)  # append in list

        # if total amount greater 0 and less than 1000, shipping charge will add 150
        if (total < 1000 and total > 0):
            shipping = 150

    final = total+shipping  # adding total price and shipping price
    # passing data through dictionary
    return render(Request, 'cart.html', {'cart': c, 'total': total, 'shipping': shipping, 'final': final})


@login_required(login_url='/login/')
def deleteCart(Request, pid):  # 11 step / pid means id
    cart = Request.session.get('cart', None)  # delete add to cart data
    if (cart):
        for key in cart.keys():
            if (str(pid) == key):
                del cart[key]
                break
        Request.session['cart'] = cart
    return redirect('/cart')


@login_required(login_url='/login/')
# 12 step / pid means id  / op= operation that which is getting cartpage ...inc for increment and dec for decrement
def updateCart(Request, pid, op):
    cart = Request.session.get('cart', None)  # delete add to cart data
    if (cart):
        for key, value in cart.items():
            if (str(pid) == key):
                if (op == 'inc'):
                    # we are increment quantity of product by 1
                    value['qty'] = value['qty']+1
                    # adding total price +price of second products
                    value['total'] = value['total']+value['price']
                # you can decrement quantity only greater than 1,quantity should have greater than1
                elif (op == 'dec' and value['qty'] > 1):
                    value['qty'] = value['qty']-1
                    # decrease price if qty will be decrement
                    value['total'] = value['total']-value['price']

                cart[key] = value  # update values
                break  # break after condition
        Request.session['cart'] = cart
    return redirect('/cart')


@login_required(login_url='/login/')
def addToWishlist(Request, pid):  # 13 step
    try:
        user = Buyer.objects.get(username=Request.user.username)
        p = Product.objects.get(id=pid)
        try:
            w = Wishlist.objects.get(user=user, product=p)
        except:
            w = Wishlist()
            w.user = user
            w.product = p
            w.save()

        return redirect("/profile/")
    except:  # admit can't create wishlist
        return redirect('/admin')


@login_required(login_url='/login/')
def deleteWishlist(Request, pid):  # 14 step / pid means id

    try:
        user = Buyer.objects.get(username=Request.user.username)
        p = Product.objects.get(id=pid)
        try:
            # wishlist is available or not
            w = Wishlist.objects.get(user=user, product=p)
            w.delete()
        except:
            pass
    except:
        pass
    return redirect('/profile')


@login_required(login_url='/login/')
def checkoutPage(Request):  # 15
    try:
        buyer = Buyer.objects.get(username=Request.user)  # find buyer
        # same details we can copy from cartpage, cart,total,shipping,final etc
        cart = Request.session.get('cart', None)
        c = []
        total = 0  # total amount
        shipping = 0  # shipping
        if (cart is not None):
            for value in cart.values():
                total = total + value['total']
                c.append(value)
            if (total < 1000 and total > 0):
                shipping = 150
        final = total+shipping  # total + shipping charge..final
        return render(Request, "checkout.html", {'user': buyer, 'cart': c, 'total': total, 'shipping': shipping, 'final': final})
    except:  # may be this is admin
        return redirect("/admin")



client = razorpay.Client(auth=(RAZORPAY_API_KEY,RAZORPAY_API_SECRET_KEY))#2 step of razor
@login_required(login_url='/login/')
def orderPage(Request):# 16 step
    if(Request.method=="POST"):
        mode = Request.POST.get("mode")
        user = Buyer.objects.get(username=Request.user.username)#getting username from Buyers
        cart = Request.session.get('cart',None)#getting cart data or not
        
        if(cart is None):#if cart is empty so redirect cart page
            return redirect("/cart")
        else:#if cart is not None means any product exists in cart
            check = Checkout()#call checkout table
            check.user = user#checkout username= Buyer username
            total = 0 #total amount from cart page
            shipping = 0# shipping is same code from cart
            for value in cart.values():#taking values from cart products
                total = total + value['total']#total amount+ value's total amount
            if (total < 1000 and total > 0): 
                shipping = 150
            final = total+shipping# checkout final = total +shiping charge
            check.total = total # checkout total = total
            check.shipping = shipping# check.shipping
            check.final=final# save checkout final= final
            check.save()# save all details in Checkout table in admin page ....check it 
            for value in cart.values():
                cp = CheckoutProduct()#call checkoutPrdouct table from models
                cp.checkout = check# checkProduct saves Checkout details through Foreign key
                cp.p = Product.objects.get(id=value['pid'])# call Product table from model through foreign key
                cp.qty = value['qty']#getting qt from checkoutproduct
                cp.total = value['total']#getting total from checkoutproduct
                cp.save()

            Request.session['cart']={}#after placed order cart will be empty
                    #for email 
            subject = f'{user.name.capitalize()}, Your Order has been Placed : Team Indian_shop'
            message = 'Thank You to Shop with us,Now Your Order has been placed. You Can Track Your Order on Profile Page.\n\nAny Query:\nEmail-id- rishithebackend@gmail.com'# sending email for infrom order placed
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email,]# whom do you want to send email ? "user.email" user means Buyer
            send_mail( subject, message, email_from, recipient_list )#No change
            
            if(mode=="COD"):#checking mode of payment from checkout page    
                return redirect("/confirmation/")
            
            else: # if payment mode is net banking
                orderAmount = check.final*100#razarpay accept money in paise suppose you have a 500 rupee (50*100 paise) =500 rupee
                orderCurrency = "INR" #Indian national rupees
                paymentOrder = client.order.create(dict(amount=orderAmount,currency=orderCurrency,payment_capture=1))# capture 1 means dashboard will show you
                paymentId = paymentOrder['id']
                
                check.save()
                return render(Request,"pay.html",{
                    "amount":orderAmount,
                    "api_key":RAZORPAY_API_KEY,
                    "order_id":paymentId,
                    "User":user
                }) #data is going through dictionary  
               
    else:
        return redirect("/checkout")
    

@login_required(login_url='/login/')#23 step
def paymentSuccess(request,rppid,rpoid,rpsid):
    buyer = Buyer.objects.get(username=request.user)
    check = Checkout.objects.filter(user=buyer)
    check=check[::-1]#last payment
    check=check[0]
    check.paymentmode=1#paymentmode is 1 means Netbanking we definded in models
    check.rppid=rppid
    # check.rpoid=rpoid// not need
    # check.rpsid=rpsid
    check.paymentstatus=1
    check.save()
    return redirect('/confirmation/')
    
    
    
    
    
@login_required(login_url='/login/')
def confirmationPage(Request):# 17 step
    return render(Request,'confirmation.html')

def contactPage(Request):# 18 step
    if (Request.method=="POST"):
        name=Request.POST.get('name')
        email=Request.POST.get('email')
        phone=Request.POST.get('phone')
        subject=Request.POST.get('subject')
        message=Request.POST.get('message')
        
        if (phone>='0' and phone<='9'):#phone number must be integer 
            c= Contact()
            c.name=name
            c.email=email
            c.phone=phone
            c.subject=subject
            c.message=message
            c.save()
            subject = 'One Query is received : Team Indian_shop'
            message = f'{c.name.capitalize()} has one Query for You.\n{c.name.capitalize()}\n{c.email.capitalize()}\n{c.phone.capitalize()}\n{c.subject.capitalize()}\n{c.message.capitalize()}\n\nThank Your Receving Indian_shop Contact Query!!!'#this is for send contact query in Admin page
            email_from = settings.EMAIL_HOST_USER
            recipient_list = ['rishithebackend@gmail.com',]# this email for receiving contact Query in Admin email
            send_mail( subject, message, email_from, recipient_list )#No change
            
            messages.success(Request,"Thank you to Share Your Feedback with Us! Our Team will Contact You Soon!!")
        else: 
            messages.error(Request,'Phone number must be Integer!!')
    return render(Request,'contact.html')


def searchPage(Request):#19 step
    if Request.method=='POST':
        search=Request.POST.get('search')
        data = Product.objects.filter(Q(name__icontains=search)|
                                      Q(color__icontains=search)|
                                      Q(size__icontains=search)|
                                      Q(stock__icontains=search)|
                                      Q(description__icontains=search)
                                      )
        maincategory = Maincategory.objects.all()
        subcategory = Subcategory.objects.all()
        brand = Brand.objects.all()
    return render(Request, "shop.html", {'data': data, 'maincategory': maincategory, 'subcategory': subcategory, 'brand': brand, 'mc': 'All', 'sc': 'All', 'br': 'All'})
    

def forgetUsername(Request):#20 step ...Email process starts
    if (Request.method=='POST'):
        username=Request.POST.get('username')
        try:
            user= User.objects.get(username=username)
            if (user.is_superuser):
                return redirect('/admin')
            else:
                buyer=Buyer.objects.get(username=username)
                otp= randrange(100000,999999)
                buyer.otp=otp
                buyer.save()
                subject = 'OTP for Password Reset : Team Indian_shop'
                message = 'OTP for Password Reset is '+str(otp)+' : Team Indian_shop.'# OTP needs to convert string formate for sending email
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [buyer.email,]# whom do you want to send email ? "buyer.email"
                send_mail( subject, message, email_from, recipient_list )#No change
                Request.session['resetuser']=username#this is for save username for otp accepting time
                
                return redirect('/forget-otp/') # OTP section             

        except:
            messages.error(Request,'Invalid Username')
            
    
    return render(Request,'forget-username.html')

#go to google and search 'sending mail in django' click on greeksforgreeks.org and copy some code and paste it top and in function top , settings file paste some files


def forgetOTP(Request):#21 step
    if (Request.method=='POST'):
        otp=Request.POST.get('otp')
        username=Request.session.get('resetuser',None)
        if (username):#when you are following all process
            if (len(otp)==6):#length must be 6 otherwise Invalid otp
                buyer=Buyer.objects.get(username=username)
                if(int(otp)==buyer.otp):#opt in integer for compare
                    return redirect("/forget-password/")
            else:
                messages.error(Request,"Invalid OTP")
        else:#if you enter direct this url
            messages.error(Request,'UnAuthorized!!!')
    return render(Request,'forget-otp.html')



def forgetPassword(Request):#22 step
    if (Request.method=='POST'):
        password=Request.POST.get('password')
        cpassword=Request.POST.get('cpassword')
        username=Request.session.get('resetuser',None)#for getting username
        if (password==cpassword):
            user= User.objects.get(username=username)
            user.set_password(password)
            user.save()
            return redirect('/login/')
        else:
            messages.error(Request,'Password and Confirm Password does not match!!!')
    return render(Request,"forget-password.html")
#process of changing password in django from website on google and copy paste her
