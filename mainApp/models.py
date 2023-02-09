from email.policy import default
from enum import unique
from django.db import models

class Maincategory(models.Model):#which type of your Maincategory like Male Product,Female,Kids
    id= models.AutoField(primary_key=True)
    name=models.CharField(max_length=40)
    
    def __str__(self):
        return self.name
    
class Subcategory(models.Model):# subcategory means which type of category like shoes,shirt,tshirt etc
    id= models.AutoField(primary_key=True)
    name=models.CharField(max_length=40)
    
    def __str__(self):
        return self.name



class Brand(models.Model):#which brand like Nike,Mufti,Puma etc
    id= models.AutoField(primary_key=True)
    name=models.CharField(max_length=40)
    
    def __str__(self):
        return self.name
    
    

class Product(models.Model):#Product details 
    id= models.AutoField(primary_key=True)
    name=models.CharField(max_length=50)    #if you want to delete Maincategories products in one click so You will use (models.CASCADE) and if you don't want the Maincategory to be deleted so use(models.PROTEST)
    #models.SETDEFAULT for by default
    maincategory=models.ForeignKey(Maincategory,on_delete= models.CASCADE)
    subcategory=models.ForeignKey(Subcategory,on_delete= models.CASCADE)
    brand=models.ForeignKey(Brand,on_delete= models.CASCADE)
    color= models.CharField(max_length=20)
    size= models.CharField(max_length=20)
    stock=models.CharField(max_length=20,default='In stock',null=True,blank=True)    
    description=models.TextField()
    baseprice= models.IntegerField()
    discount= models.IntegerField(default=0,null=True,blank=True) 
    finalprice= models.IntegerField()
    pic1= models.ImageField(upload_to="uploads",default="",null=True,blank=True)
    pic2= models.ImageField(upload_to="uploads",default="",null=True,blank=True)
    pic3= models.ImageField(upload_to="uploads",default="",null=True,blank=True)
    pic4= models.ImageField(upload_to="uploads",default="",null=True,blank=True)
       
    def __str__(self):
        return self.name

class Buyer(models.Model):#Buyer details
    id= models.AutoField(primary_key=True)
    name=models.CharField(max_length=40)
    username=models.CharField(unique=True,max_length=50)
    email=models.EmailField(max_length=60)
    phone= models.CharField(max_length=15)
    addressline1= models.CharField(max_length=150)
    addressline2= models.CharField(max_length=150,default='')
    addressline3= models.CharField(max_length=150,default='')
    pin= models.CharField(max_length=50)
    city=models.CharField(max_length=50)
    state=models.CharField(max_length=50)
    pic= models.ImageField(upload_to="uploads",default='',null=True,blank=True)
    otp= models.IntegerField(default=-3434343)#you have to insert default values otherwise table will not accept it, we want positive otp number so we are using negative num in default. Doesn't matter whatever num
    
    def __str__(self):
        return str(self.id)+" " +self.username
    
    
class Wishlist(models.Model):#for creating wishlist table 
    id= models.AutoField(primary_key=True)
    user= models.ForeignKey(Buyer,on_delete=models.CASCADE)
    product= models.ForeignKey(Product,on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.id)+" " +self.user.username+" "+self.product.name
    
    

#we are creating option that payment,mode,status but before create checkout table you have to defind choices
status = ((0,"Order Placed"),(1,"Not Packed"),(2,"Packed"),(3,"Ready to Ship"),(4,"Shipped"),(5,"Out For Delivery"),(6,"Delivered"),(7,"Cancelled"))
payment = ((0,"Pending"),(1,"Done"))
mode = ((0,"COD"),(1,"Net Banking"))


class Checkout(models.Model):
    id= models.AutoField(primary_key=True)
    user= models.ForeignKey(Buyer,on_delete=models.CASCADE)
    total= models.IntegerField()
    shipping= models.IntegerField()
    final= models.IntegerField()
    rppid= models.CharField(max_length=30,default="",null=True,blank=True)#online payment Razerpay
    date= models.DateTimeField(auto_now=True)#auto now means created time when table will create time auto set current time
    paymentmode=models.IntegerField(choices=mode,default=0)#payment choice COD or Netbanking
    paymentstatus= models.IntegerField(choices=payment,default=0)# Pending or Done Payment
    orderstatus= models.IntegerField(choices=status, default=0)#payment status ...like packed,ready to ship, deliverd etc
    
    def __str__(self):
        return str(self.id)+" "+self.user.username
    
class CheckoutProduct(models.Model):
    id= models.AutoField(primary_key=True)
    checkout= models.ForeignKey(Checkout,on_delete=models.CASCADE)#connect checkout table
    p= models.ForeignKey(Product,on_delete=models.CASCADE)#connect product table
    qty = models.IntegerField(default=1)
    total = models.IntegerField()
    
    def __str__(self):
        return str(self.id)+" "+str(self.checkout.id)
    
    
contactstatus=((0,"Active"),(1,'Done'))
class Contact(models.Model):
    id= models.AutoField(primary_key=True)
    name=models.CharField(max_length=30)
    email=models.EmailField(max_length=60)
    phone= models.CharField(max_length=15)
    subject= models.CharField(max_length=50)
    message= models.TextField()
    status= models.IntegerField(choices=contactstatus,default=0)
    date= models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.id)+" ,"+self.name+" ,"+ self.subject