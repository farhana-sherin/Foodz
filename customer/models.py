from django.db import models

from users.models import User
from restaurent.models import Store, FoodItem


ORDER_STATUS_CHOICES=(
    ('PALCEORDER','PL'),
    ('ACCEPT','AC'),
    ('SHIPPED','SH'),
    ('ONTHEWAY','DI'),
    ('DELIVERD','DL'),
    ('CANCELED','CL')
    
)


class Customer(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email
    
class Cart(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    store=models.ForeignKey(Store, on_delete=models.CASCADE)
    item=models.ForeignKey(FoodItem,on_delete=models.CASCADE ,related_name='item')
    amount=models.IntegerField()
    quantity=models.IntegerField()


    class Meta:
        db_table='cart'
        verbose_name='cart'
        verbose_name_plural='carts'
        ordering=['-id']

    def __str__(self):
        return self.item.name
    

    
class CartBill(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    delivery_charge=models.IntegerField(default=0 ,null=True,blank=True)
    offer_amount=models.FloatField(default=0)
    coupe_code=models.CharField(max_length=255, null=True,blank=True)



    class Meta:
        db_table='cart_bill'
        
        verbose_name='cart_bill'
        verbose_name_plural='cart_bills'
        ordering=['-id']

    def __str__(self):
        return self.customer.user.email

class Address(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    address=models.CharField(max_length=255)
    appartment=models.TextField()
    landmark=models.CharField(max_length=255)
    address_type=models.CharField(max_length=255)
    is_selected = models.BooleanField(default=False)


    class Meta:
        db_table='address'
        verbose_name='address'
        verbose_name_plural='addresss'
        ordering=['-id']

    def __str__(self):
        return self.customer.user.email
    


class Offers(models.Model):
    offer=models.FloatField()
    code=models.CharField(max_length=255)
    description=models.CharField(max_length=255)
    is_pecentage=models.BooleanField(default=False)



    class Meta:
        db_table='offers'
        verbose_name='offers'
        verbose_name_plural='offerss'
        ordering=['-id']

    def __str__(self):
        return self.code
    

class Order(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    store=models.ForeignKey(Store,on_delete=models.CASCADE ,null=True,blank=True)
    
    address=models.ForeignKey(Address,on_delete=models.CASCADE)
    subtotal=models.FloatField()
    total=models.FloatField()
    delivery_charge=models.IntegerField(default=0)
    order_id=models.CharField(max_length=255)
    status=models.CharField(max_length=255 ,choices=ORDER_STATUS_CHOICES)



    
    class Meta:
        db_table='order'
        verbose_name='orders'
        verbose_name_plural='orderess'
        ordering=['-id']


    def __str__(self):
        return self.order_id

class OrderItem(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    store=models.ForeignKey(Store, on_delete=models.CASCADE)
    item=models.ForeignKey(FoodItem,on_delete=models.CASCADE)
    amount=models.IntegerField()
    quantity=models.IntegerField()
    order=models.ForeignKey(Order ,on_delete=models.CASCADE)


    class Meta:
        db_table='order_item'
        verbose_name='order item'
        verbose_name_plural='order items'
        ordering=['-id']

    def __str__(self):
        return f"{self.quantity} x {self.item.name}"


    



    

    








    

