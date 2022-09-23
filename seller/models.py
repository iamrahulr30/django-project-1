from django.db import models
from django.db.models.deletion import SET_DEFAULT, SET_NULL
from user.models import User
from django.utils import timezone

class Sellerprofile(models.Model):
    author = models.OneToOneField(User,on_delete=models.CASCADE)
    proimage = models.ImageField(default='default.jpg', upload_to='profile_pics')
    shop_name = models.CharField(max_length=150,unique=True)
    Business_mail = models.EmailField()

    def __str__(self):
        return f"{self.author} - {self.shop_name} "
    
class tag(models.Model):
    name = models.CharField(max_length=2000)

    def __str__(self):
        return f"{self.name}"


class Product(models.Model):
    author = models.ForeignKey(Sellerprofile,on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    title = models.CharField(max_length=200)
    price = models.IntegerField()
    detials = models.TextField()
    quantity = models.PositiveSmallIntegerField()
    filter = models.ManyToManyField(tag)
    date_time = models.DateTimeField(default=timezone.now)

    
    def __str__(self):
        return f"{self.author.author} - {self.author.shop_name} - {self.title} - {self.price} - {self.pk}"


