from django import forms
from .models import Product ,Sellerprofile
from user.models import order

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title','image','price','detials','quantity']

class SellerprofileUpdateform(forms.ModelForm):
    class Meta:
        model = Sellerprofile
        fields = ['shop_name','Business_mail','proimage']
