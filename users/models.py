from django.db import models
from django.core.exceptions import ValidationError
from orders.models import Cart
 
class User(models.Model):
    first_name = models.CharField(max_length=50, blank=False, null=False)
    last_name = models.CharField(max_length=50, blank=False, null=False)
    email = models.EmailField(unique=True, blank=False, null=False)
    username = models.CharField(max_length=50, unique=True, blank=False, null=False)
    password = models.CharField(max_length=128, blank=False, null=False)
 
    def __str__(self):
        return self.username
 
    def clean(self):
        # Check that all fields are filled in
        if not self.first_name:
            raise ValidationError('First name is required')
        if not self.last_name:
            raise ValidationError('Last name is required')
        if not self.email:
            raise ValidationError('Email is required')
        if not self.username:
            raise ValidationError('Username is required')
        if not self.password:
            raise ValidationError('Password is required')





class Category(models.Model):
    name = models.CharField(max_length=200,blank=False,unique=True)
    imageUrl = models.TextField(unique=True,blank=False,null=True)

    def __str__(self):
        return self.name




class Dish(models.Model):
    name = models.CharField(max_length=200,blank=False,unique=True)
    price = models.IntegerField(blank=False,null=False)
    description = models.TextField(blank=True,null=True)
    imageUrl = models.TextField(blank=False)
    is_gluten_free = models.BooleanField(default=False)
    is_vegetarian = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)




class Item(models.Model):
    dish=models.ForeignKey(Dish,default="",on_delete=models.CASCADE)
    cart=models.ForeignKey(Cart, related_name='item' ,default="", on_delete=models.CASCADE)
    amount=models.IntegerField(default=0)
