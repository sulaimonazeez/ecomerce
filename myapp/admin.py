from django.contrib import admin
from .models import Category,Products, UserProfile, Cart, CartItem, Order, Payment
# Register your models here.
admin.site.register(Category)
admin.site.register(Products)
admin.site.register(UserProfile)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(Payment)