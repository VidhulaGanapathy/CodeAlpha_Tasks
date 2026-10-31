from django.contrib import admin
from .models import Product, Order, OrderItem   # the dot means "from this same folder"

admin.site.register(Product)     # show the Product table in the admin panel
admin.site.register(Order)
admin.site.register(OrderItem)