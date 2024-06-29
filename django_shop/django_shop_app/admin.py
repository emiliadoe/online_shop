from django.contrib import admin
from .models import Product, Rating, CartItem


# Register your models here.

admin.site.register(Product)
admin.site.register(Rating)
admin.site.register(CartItem) 