from django.contrib import admin
from .models import Product, Rating, Category


# Register your models here.

admin.site.register(Product)
admin.site.register(Rating)
""" admin.site.register(Category) """