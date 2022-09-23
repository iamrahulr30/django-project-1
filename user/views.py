from django.contrib.auth.forms import UsernameField
from django.core import paginator
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
# from sqlalchemy import null
from user.models import User, order
from django.shortcuts import render, redirect
from .forms import UserRegisterForm, UserUpdateForm, Orderform,Usertoseller
from django.contrib import messages
from seller.models import Product, Sellerprofile
from user.models import order
from .models import *
from django.views.generic import CreateView, FormView, UpdateView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.contrib.messages.views import SuccessMessageMixin
from .filters import Productfilter,shopfilter
from django.core.paginator import Paginator


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            form.save()
            messages.success(request, f'Account created for {username}')
            return redirect('login')
    else:
        form = UserRegisterForm()
    context = {
        'title': 'Register',
        'form': form
    }
    return render(request, 'user/register.html', context)


def home(request):
    products = Product.objects.all().order_by('?')
# -date_time
    myFilter = Productfilter(request.POST, queryset=products)
    products = myFilter.qs

    #pagination
    paginator = Paginator(products, 8) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'title': 'Home',
        'products': products,
        'myFilter': myFilter,
        'page_obj': page_obj
    }
    return render(request, 'user/home.html', context)


class HomeView(ListView):
    model = Product
    template_name = 'user/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'products'
    paginate_by = 9

    def get_queryset(self):
        return Product.objects.all().order_by('?')


class Shopview(ListView):
    model = Sellerprofile
    template_name = 'user/shops.html'
    context_object_name = 'shops'

    def get_queryset(self):
        return Sellerprofile.objects.all().order_by('?')


def shops(request):
    shops = Sellerprofile.objects.all().order_by('?')

    myFilter = shopfilter(request.POST, queryset=shops)
    shops = myFilter.qs

    context = {
        'title': 'Shops',
        'shops': shops,
        'myFilter': myFilter
    }
    return render(request, 'user/shops.html', context)


def shopmain(request, shop):
    context = {
        'title': 'shopmain',
        'products': Product.objects.filter(author=Sellerprofile.objects.get(pk=shop)),
        'shop': Sellerprofile.objects.get(pk=shop)
    }
    return render(request, 'user/shoppage.html', context)


def cart(request):
    products = []
    total = 0
    for i in request.user.my_cart:
        if Product.objects.filter(pk=i):
            products.append(Product.objects.filter(pk=i))
        else:
            user = request.user
            user.my_cart.remove(i)

    for product in products:
        # total = sum(product.price)
        for i in product:
            print(i.price)
            total += i.price

    context = {
        'title': 'My Cart',
        'products': products,
        'total_price': total
    }
    return render(request, 'user/usercart.html', context)


def profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid:
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Account Updated to {username}")
            return redirect('user-profile')
    else:
        form = UserUpdateForm(instance=request.user)
    context = {
        'title': 'My Cart',
        'form': form
    }
    return render(request, 'user/profile.html', context)


class Productview(LoginRequiredMixin, SuccessMessageMixin, DetailView):
    model = Product
    template_name = 'user/product_page.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'product'


def pro_pg(request, pk):
    context = {
        'product': Product.objects.filter(pk=pk).first(),
    }
    return render(request, 'user/product_page.html', context)


def add_to_cart(request, pk):
    user = request.user
    if Product.objects.filter(pk=pk):
        user.my_cart.append(pk)
        user.save()
        messages.success(request, "Product added to cart")
        return redirect('propg', pk=pk)


def remove_from_cart(request, pk):
    user = request.user
    if Product.objects.filter(pk=pk):
        user.my_cart.remove(pk)
        user.save()
        messages.success(request, "Product removed cart")
        return redirect('user-cart')


def buy(request, pk):
    pro = Product.objects.filter(pk=pk).first()
    print(pro)
    if request.method == 'POST':
        print(request.POST)
        form = Orderform(request.POST)
        if request.user.is_anonymous == False:
            form.instance.customer = request.user
        else:
            form.instance.customer = None
        form.instance.product = pro
        print(form.instance.product)
        # orders = order(customer=form.instance.user,name=form.instance.name,product=pro,email=form.instance.email,address=form.instance.address)
        if form.is_valid:
            form.save()
            # print(order)
            messages.success(request, f"You have purchased {pro.title}")
            return redirect('user-home')
    else:
        if request.user.is_anonymous == False:
            form = Orderform(instance=request.user)
        form = Orderform()
        
    context = {
        'title': 'Purchase',
        'form': form,
        'product': Product.objects.filter(pk=pk).first()
    }
    return render(request, 'user/buy.html', context)


def buy_cart(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        for items in request.user.my_cart:
            if Product.objects.filter(pk=items):
                print(items)
                pro = Product.objects.filter(pk=items).first()
                print(pro)
                orders = order(customer=request.user,name=name,product=pro,email=email,address=address)
                orders.save()
            
        messages.success(request, "You have purchased items from your cart")
        return redirect('user-home')
    else:
        form =Orderform(instance=request.user)

    products = []
    for i in request.user.my_cart:
        if Product.objects.filter(pk=i):
            products.append(Product.objects.filter(pk=i))
        else:
            user = request.user
            user.my_cart.remove(i)
    context = {
        'form': form,
        'title': 'purchase',
        'products': products
    }
    return render(request, 'user/buycart.html', context)

def userorders(request):
    # myorders = order.objects.get(customer = request.user)
    orders = request.user.order_set.all()
    paginator = Paginator(orders,9)
    no = len(orders)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # context = {
    #     'title': '',
    #     'products': orders,
    #     'no': no,
    #     'page_obj':page_obj
    # }
    context = {
        'title': 'my orders',
        #'products': products
        'products':orders,
        'no' : no,
        'page_obj':page_obj
    }
    return render(request, 'user/myorders.html', context)

def userupdate(request):
    form = Usertoseller()
    if request.method =='POST':
        form = Usertoseller(request.POST,request.FILES)
        user= User.objects.get(pk=request.user.pk)
        form.instance.author = user
        print(user)
        if form.is_valid():
            form.save()
            user.is_seller = True
            user.save()
            messages.success(request, "Your seller account has been created")
            return redirect('seller-home')
    
    context={
        'form':form
    }
    return render(request,'user/usertoseller.html',context)


def proimg(request,pk):
    product = Product.objects.get(pk=pk)
    context={
        'product':product
    }
    return render(request,'user/proimg.html',context)
# Create your views here.
