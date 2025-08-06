from django.db import models
from store_owner.models import *

class StoreCategory(models.Model):
    name=models.CharField(max_length=50)
    image=models.ImageField(upload_to='category')

    class Meta:
        db_table='restaurent_category'
        verbose_name='store category'
        verbose_name_plural='store_categories'
        ordering= ['-id']

    def __str__(self):
        return self.name
    

class Store(models.Model):
    
    name=models.CharField(max_length=255)
    category=models.ForeignKey(StoreCategory,on_delete=models.CASCADE)
    image=models.ImageField(upload_to='store')
    short_descritpion=models.CharField(max_length=255)
    rating=models.FloatField()
    time=models.IntegerField()
    

 
   

    
   

    class Meta:
        db_table ="restaurent_store"
        verbose_name='store'
        verbose_name_plural='stores'
        ordering=['-id']


    def __str__(self):
        return self.name
    


class Slider(models.Model):
    name=models.CharField(max_length=255)
    image=models.ImageField(upload_to='slider')
    store=models.ForeignKey(Store, on_delete=models.CASCADE)


    class Meta:
        db_table ='restaurent_slider'
        verbose_name='slider'
        verbose_name_plural ='sliders'
        ordering=['-id']

    def __str__(self):
        return self.name
    


class FoodCategory(models.Model):
    name=models.CharField(max_length=255)
    store=models.ForeignKey(Store,on_delete=models.CASCADE)



    class Meta:
        db_table='food_category'
        verbose_name='food category'
        verbose_name_plural="food categories"
        ordering=['-id']
    
    def __str__(self):
        return self.name
        



class FoodItem(models.Model):
    name=models.CharField(max_length=255)
    image=models.FileField(upload_to='fooditem')
    price=models.IntegerField()
    category=models.ForeignKey(FoodCategory, on_delete=models.CASCADE, related_name='fooditem')
    store=models.ForeignKey(Store,on_delete=models.CASCADE)
    is_veg = models.BooleanField(default=False)


    class Meta:
        db_table='food_item'
        verbose_name='fooditem'
        verbose_name_plural='fooditems'
        ordering=['-id']
    

    def __str__(self):
        return self.name










        
 

    
