from django import template#this page is connected from template profile page
#and we are sharing product data through this

from mainApp.models import CheckoutProduct,Checkout,Product


register=template.Library()

@register.filter(name='checkoutProduct')# name of product 'checkoutproudcts'
def checkoutProduct(checkoutid):
    checkout= Checkout.objects.get(id=checkoutid)
    cp= CheckoutProduct.objects.filter(checkout=checkout)#checkoutid means CheckoutProduct checkoutid
    c=[]
    for item in cp:
        x = {'name':item.p.name,'maincategory':item.p.maincategory,'subcategory':item.p.subcategory,'brand':item.p.brand,'color':item.p.color,'size':item.p.size,'price':item.p.finalprice,'qty':item.qty,'total':item.total,'pic':item.p.pic1.url}#url for pic is important
        c.append(x)
    return c

#after set this page restart server 


# mode = ((0,"COD"),(1,"Net Banking"))According to this

@register.filter(name='paymentStatus')# checking payment status from models
def paymentStatus(op):# condition of payment status and through them we are showing output of mode
    if (op==0):
        return 'Pending'
    else:
        return 'Done'
  
  
# payment = ((0,"Pending"),(1,"Done"))According to this from models
  
@register.filter(name='paymentmode')# checking payment mode from models
def paymentmode(op):# condition of payment mode and through them we are showing output of mode
    if (op==0):
        return 'COD'
    else:
        return 'Net Banking'
    
    
    
# status = ((0,"Order Placed"),(1,"Not Packed"),(2,"Packed"),(3,"Ready to Ship"),(4,"Shipped"),(5,"Out For Delivery"),(6,"Delivered"),(7,"Cancelled"))
#According to status of order

@register.filter(name='orderStatus')# checking order status from models
def orderStatus(op):# condition of order status and through them we are showing output of mode
    if (op==0):
        return 'Order Placed'
    elif (op==1):
        return 'Not Packed'
    elif (op==2):
        return 'Packed'
    elif (op==3):
        return 'Ready to Ship'
    elif (op==4):
        return 'Shipped'
    elif (op==5):
        return 'Out For Delivery'
    elif (op==6):
        return 'Delivered'
    else:
        return "Cancelled"
    
    
#after that check to change your paymentmode,orderstatus,paymentstatus through admin page that page is working correctly or not