from collections import defaultdict
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.fields.reverse_related import OneToOneRel
from django.utils import timezone
#from django.urls import reverse


class User(AbstractUser):
    is_seller = models.BooleanField(default=False)
    my_cart = models.JSONField(default=list)
    email = models.EmailField()
    image = models.ImageField(default='userdef.jpg',upload_to='profile_pics')

    def __str__(self):
        return f"{self.username}-{self.pk}"

from seller.models import Product, Sellerprofile


class order(models.Model):
    status = (
            ('delivered','delivered'),
            ('pending','pending'),
            ('out for delivery','out for delivery'))


    customer = models.ForeignKey(User,null=True,on_delete=models.SET_NULL)
    name = models.CharField(max_length=200)
    product = models.ForeignKey(Product,null=True,on_delete=models.SET_NULL)
    email = models.EmailField(null=True,blank=True)
    address = models.TextField()
    delivered = models.CharField(max_length=1000,choices=status,default='pending')
    date_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.pk} - {self.name}  -  {self.product}|{self.product.author.shop_name}  ⏰: {self.date_time}"