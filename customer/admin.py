from django.contrib import admin

from customer.models import Customer
from customer.models import Cart
from customer.models import CartBill
from customer.models import Address
from customer.models import Offers
from customer.models import Order
from customer.models import OrderItem



admin.site.register(Customer)
admin.site.register(Cart)
admin.site.register(CartBill)
admin.site.register(Address)
admin.site.register(Offers)
admin.site.register(Order)
admin.site.register(OrderItem)



