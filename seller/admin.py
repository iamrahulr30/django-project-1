from django.contrib import admin
from seller.models import Product,Sellerprofile,tag

admin.site.register(tag)
admin.site.register(Product)
admin.site.register(Sellerprofile)

# Register your models here.
