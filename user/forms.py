from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User,order
from seller.models import Sellerprofile


class UserRegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email','image']

class Usertoseller(forms.ModelForm):
    
    class Meta:
        model = Sellerprofile
        fields = '__all__'
        exclude = ['author']

class Orderform(forms.ModelForm):

    class Meta:
        model = order
        fields = ['name','email','address']

        