from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.conf import settings


from customer.models import *
from users.models import User



class AddressSerializer(ModelSerializer):
    class Meta:
        fields = ['id', 'address', 'appartment', 'landmark', 'address_type']
        model = Address