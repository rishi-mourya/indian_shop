from django.contrib import admin
from mainApp.models import*

admin.site.register((Maincategory,Subcategory,Brand,Product,Buyer,Wishlist,Checkout,CheckoutProduct,Contact))