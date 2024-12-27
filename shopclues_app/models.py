from django.db import models
import datetime
import os
from django.contrib.auth.models import User

# Create your models here.

def getFileName(request,filename):
    now_time=datetime.datetime.now().strftime("%Y%m%d%H:%M:%S")
    new_filename="%s%s"%(now_time,filename)
    return os.path.join('uploads/',new_filename)



class Category(models.Model):
    name=models.CharField(max_length=150,null=False,blank=False)
    image=models.ImageField(upload_to=getFileName,null=True,blank=True)
    description=models.TextField(max_length=500,null=False,blank=False)
    status=models.BooleanField(default=False,help_text="0-show.1-Hidden")
    created_at=models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.name


class Products(models.Model):
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    name=models.CharField(max_length=150,null=False,blank=False, unique=True)
    vender=models.CharField(max_length=150,null=False,blank=False)
    product_image=models.ImageField(upload_to=getFileName,null=True,blank=True)
    quantity=models.IntegerField(null=False,blank=False)
    original_price=models.IntegerField(null=False,blank=False)
    selling_price=models.IntegerField(null=False,blank=False)
    description=models.TextField(max_length=500,null=False,blank=False)
    status=models.BooleanField(default=False,help_text="0-show.1-Hidden")
    trending=models.BooleanField(default=False,help_text="0-default.1-trending")
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
    

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)  # Ensure 'quantity' exists here
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.product.name}'
    
    @property
    def total_cost(self):
        return self.quantity*self.product.selling_price
    
   
    
class Favourite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.product.name}'
    
    
    








    
       





