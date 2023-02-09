
from django.contrib import admin
from django.urls import path
from django.conf import settings#You have to import this file for  run below code
from django.conf.urls.static import static#You have to import this file too for  run below code
#static means images
from mainApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home),
    path('shop/<str:mc>/<str:sc>/<str:br>/',views.shopPage),#mc=maincategory,sc=subcategory,br=subcategory because we are taking all category when we call shop page
    path('single-product/<int:id>/',views.singleProduct),
    path('login/',views.loginPage),
    path('signup/',views.signupPage),
    path('profile/',views.profilePage),
    path('logout/',views.logoutPage),
    path('update-profile/',views.updatePage),
    path('add-to-cart/<int:id>/',views.addToCart),
    path('cart/',views.cartPage),
    path('delete-cart/<int:pid>/',views.deleteCart),
    path('update-cart/<int:pid>/<str:op>/',views.updateCart),
    path('add-to-wishlist/<int:pid>/',views.addToWishlist),
    path('delete-wishlist/<int:pid>/',views.deleteWishlist),
    path('checkout/',views.checkoutPage),
    path('order/',views.orderPage),
    path('confirmation/',views.confirmationPage),
    path('contact/',views.contactPage),
    path('search/',views.searchPage),
    path('forget-username/',views.forgetUsername),
    path('forget-otp/',views.forgetOTP),
    path('forget-password/',views.forgetPassword),
    path('paymentSuccess/<str:rppid>/<str:rpoid>/<str:rpsid>',views.paymentSuccess),
    
    
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)#This file for uploading images url

