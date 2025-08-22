from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.conf import settings


from customer.models import *
from users.models import User
from restaurent.models import *


class CustomerSerializer(ModelSerializer):
    class Meta:
        fields = ['id', 'user']
        model = Customer
class AddressSerializer(ModelSerializer):
    class Meta:
        fields = ['id', 'address', 'appartment', 'landmark', 'address_type']
        model = Address


class CartSerializer(ModelSerializer):
    class Meta:
        fields = ['id', 'customer', 'store', 'item', 'amount', 'quantity']
        model = Cart

class CartBillSerializer(ModelSerializer):
    class Meta:
        fields = ['id', 'customer', 'delivery_charge', 'offer_amount', 'coupe_code']
        model = CartBill

class StoreSerializer(ModelSerializer):
    class Meta:
        fields = ['id', 'name', 'category', 'image', 'short_descritpion', 'rating', 'time']
        model = Store

class OffersSerializer(ModelSerializer):
    class Meta:
        fields = ['id', 'code', 'offer', 'is_pecentage']
        model = Offers

class foodItemSerializer(ModelSerializer):
    class Meta:
        fields = ['id', 'name', 'price', 'image', 'description']
        model = FoodItem

class OrderSerializer(ModelSerializer):
    class Meta:
        fields = ['customer','store','address','subtotal','total','delivery_charge','order_id','status']
        model = Order
class StoreCategorySerializer(ModelSerializer):
    class Meta:
        fields = ['id', 'name', 'image']
        model = StoreCategory

class FoodCategorySerializer(ModelSerializer):
    class Meta:
        fields = ['id', 'store', 'name']
        model = FoodCategory

class FoodItemSerializer(ModelSerializer):
    class Meta:
        fields = ['id', 'name', 'price', 'image', 'category', 'store', 'is_veg']
        model = FoodItem
class SliderSerializer(ModelSerializer):
    
    class Meta:
        fields = [ 'name', 'image', 'store']
        model = Slider





