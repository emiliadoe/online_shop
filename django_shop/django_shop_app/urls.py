"""
URL configuration for django_shop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views


"""    path('', views.overview_list, name='overview-list'),
 """

urlpatterns = [
    path('', views.overview_list, name='overview'),
    path('<int:pk>/', views.product_detail, name='product-detail'),
    path('<int:pk>/vote/<str:up_or_down>/', views.rate, name='product-rating'),
    path('add-to-cart/<int:pk>/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.cart_detail, name='cart-detail'),
    path('search/', views.product_search, name='product-search'),

]
