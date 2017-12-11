from django.contrib import admin
from .models import CartItem, Cart
from .models import City
# Register your models here.
admin.site.register(CartItem)
admin.site.register(Cart)
admin.site.register(City)