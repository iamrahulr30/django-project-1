from django.core import paginator
from django.db.models.query import  QuerySet
from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404,redirect
from django.db import models
from django.contrib import messages
from django.views.generic import ListView, UpdateView, DeleteView, CreateView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
# from django.shortcuts import , render
from .forms import ProductForm, SellerprofileUpdateform
from django.urls import reverse_lazy, reverse
from django.core.paginator import Paginator
#user imports
from .models import Product, Sellerprofile
from seller.models import User
from user.filters import OrderFilter
from .func import sellerpages
from user.models import order
# from django.db.models.utils import list_to_queryset
import  matplotlib.pyplot as plt
from matplotlib import dates as mda#*****************
import base64
from io import BytesIO#**********


@sellerpages
def newproduct(request):
    if request.method == 'POST':
        # images = request.FILES.getlist()
        form = ProductForm(request.POST, request.FILES)
        form.instance.author = request.user.sellerprofile
        form.instance.shop = request.user.sellerprofile.shop_name
        if form.is_valid:
            form.save()
            product = form.cleaned_data.get('title').title()
            messages.success(request, f"{product} Posted")
            return redirect('newproduct')
    else:
        form = ProductForm()
    context = {
        'form': form,
        'title': 'New Product'
    }
    return render(request, 'seller/newpro.html', context)


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Product
    fields = ['title', 'image', 'price', 'tax', 'detials', 'quantity']
    success_url = "/product"
    success_message = f"Product has been Updated"
    success_url = reverse_lazy('seller-home')

    def form_valid(self, form):
        form.instance.author = self.request.user.sellerprofile
        form.instance.shop = self.request.user.sellerprofile.shop_name
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user.sellerprofile == post.author:
            return True
        return False


@sellerpages
def sellerorder(request):
    products = []
    user = request.user.sellerprofile
    orders = order.objects.all().order_by('-delivered','-date_time')
    orderfilt = OrderFilter(request.POST,queryset=orders)
    orders = orderfilt.qs
    # for i in orders:
    #     print(i)
    # print("*************************************************************")
    for i in orders:
        if i.product.author == user:
            products.append(i)
            # print(i)

    paginator = Paginator(products,20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # myfilt = OrderFilter(request.GET, queryset=products)
    total = delivered = out_for_deliverey = pending = 0    #  myfilt = OrderFilter(request.GET, queryset=products
    for ord in products:                                   #  products = myfilt.qs
        if ord.delivered == "delivered":
            delivered += 1
        elif ord.delivered == "out for delivery":
            out_for_deliverey += 1
        elif ord.delivered == 'pending' :
            pending += 1
        

    context = {
        'title': 'Home',
        'orderfilt' : orderfilt,
        'orders': products,
        'total' : len(products),
        'delivered' : delivered,
        'out_for_delivery' : out_for_deliverey,
        'pending' : pending,
        'page_obj' : page_obj
    }
    return render(request, 'seller/order.html', context)

def ordel(request,pk):
    orders = order.objects.get(pk=pk)
    status = (('delivered','delivered'),
             ('pending','pending'),
             ('out for delivery','out for delivery'))
    if orders.delivered == 'delivered':
        orders.delivered = 'pending'
        orders.save()
        messages.success(request, f"order updated")
        return redirect('seller-order')
    elif orders.delivered == 'out for delivery':
        orders.delivered = 'delivered'
        orders.save()
        messages.success(request, f"order updated")
        return redirect('seller-order')
    elif orders.delivered == 'pending':
        orders.delivered = 'out for delivery'
        orders.save()
        messages.success(request, f"order updated")
        return redirect('seller-order')

    context={
    }
    return render(request, 'seller/upgradeorder.html', context)

class OrderUpdateView(LoginRequiredMixin,UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = order
    fields = ['name', 'address', 'product', 'delivered']
    template_name = 'seller/orde.html'
    success_url = reverse_lazy('seller-order')
    success_message = f"Order updated"

    def test_func(self):
        post = self.get_object()
        print(self.request.user.sellerprofile)
        print(post.product.author)
        if self.request.user.sellerprofile == post.product.author or self.request.user == post.customer:
            
            return True
        return False


# orders(author=pro.author, name=name, email=email, address=address,
        # title=pro.title, image=pro.image, product_id=pk, shop=pro.shop, total_price=pro.price,
        # tax=pro.tax, detials=pro.detials, quantity=1,delivered=True)


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = order
    success_url = "/product"
    success_message = f"Product has been Deleted"

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


# def Profile(request):
#     if request.method == 'POST':

#         p_form = SellerprofileUpdateform(request.POST, request.FILES, instance=request.user.profile)
#         if u_form.is_valid() and p_form.is_valid():
#             u_form.save()
#             p_form.save()
#             return redirect('seller-home')
#     else:
#         u_form = UserUpdateForm(instance=request.user)
#         p_form = ProfileUpdateform(instance=request.user.profile)
#     context = {
#         'u_form': u_form,
#         'p_form': p_form,
#         'title': 'Home'
#     }
#     return render(request, 'seller/home.html', context)


# def product(request):
#     if request.method == 'POST':
#         form = ProductForm(request.POST)
#         if form.is_valid():
#             form.instance.author = request.user
#             form.save()
#             username = form.cleaned_data.get('username')
#             messages.success(request, f'Product Posted')
#             return redirect('seller-product')
#     else:
#         form = ProductForm()
#     user = request.user
#     context = {
#         'posts': Product.objects.filter(author=user),
#         'form': form,
#         'title': 'product'
#     }
#     return render(request, 'seller/product.html', context)

@sellerpages
def sellerhome(request):
    product = request.user.sellerprofile.product_set.all().order_by('-title')
    no = len(product)
    paginator = Paginator(product,9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'title': 'Home',
        'products': product,
        'no': no,
        'page_obj':page_obj
    }
    return render(request, 'seller/home.html', context)





# class Sellerorder(LoginRequiredMixin,ListView):
#     model = Product
#     template_name = 'seller/order.html'  # <app>/<model>_<viewtype>.html
#     context_object_name = 'orders'
#     paginate_by = 8

#     def get_queryset(self):
#         user = self.request.user.sellerprofile
#         return orders.objects.filter(author=user)

    # def get_context_data(self, **kwargs):
    #     headings = {'delivered','name','email','address','author','product_id','title','total_price','quantity','image.url','date_time','shop'}
    #     return headings

@sellerpages
def SellerUpdate(request):
    if request.method == 'POST':
        user = request.user.sellerprofile
        form = SellerprofileUpdateform(request.POST, request.FILES, instance=request.user.sellerprofile)
        if form.is_valid():
            products = list()
            if Product.objects.filter(author=user):
                products.append(Product.objects.filter(author=user))
                for i in products:
                    print(products)
                    form.save()
                    for o in i:
                        newname = form.cleaned_data.get('shop_name')
                        o.shop = newname
                        print(" here's the name ")
                        o.save()
                    messages.success(request, f"Account Updated to {newname}")
                    return redirect('seller-update')
    else:
        form = SellerprofileUpdateform(instance=request.user.sellerprofile)
    context = {
        'form': form,
        'title': 'Sellerprofile'
    }
    return render(request, 'seller/profile.html', context)

    # def get_success_url(self):
    #     return reverse('seller-home')


@sellerpages
def propage(request, pk):
    user = request.user.sellerprofile
    product = Product.objects.filter(pk=pk).first()
    if product.author != user:
        return HttpResponse("you are not authorized to access this page")
    context = {
        'product': Product.objects.filter(pk=pk).first(),
    }
    return render(request, 'seller/pro.html', context)


def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer,format='png')
    buffer.seek(0)
    image = buffer.getvalue()
    graph = base64.b64encode(image)
    graph =graph.decode('utf-8')
    buffer.close()
    return graph

@sellerpages
def sellergraph(request):
    f = order.objects.all()
    date,no,orders,dct = [],[],[],{}
    for i in f:
        if i.product.author.author == request.user:
            orders.append(i)
    for i in orders:
        if i.date_time.date() not in dct:
            dct[i.date_time.date()] = 1
        else:
            dct[i.date_time.date()] += 1
    for i,j in dct.items():
        date.append(i)
        no.append(j) 

    plt.switch_backend('AGG')
    plt.style.use('fivethirtyeight')
    plt.figure(figsize=(8,5))
    plt.title('orders per day')
    plt.plot_date(date,no,color='#ff6666',linestyle='solid',linewidth=2)
    plt.xticks(rotation=45)
    date_format = mda.DateFormatter(" %b,%d,%Y ")#month,day,year
    plt.gca().xaxis.set_major_formatter(date_format)

    # plt.gcf().autofmt_xdate()#gif current figure
    plt.xlabel('date')
    plt.ylabel('orders')
    plt.tight_layout()
    graph =  get_graph()
    context={
        'dct':dct,
        'chart':graph
    }
    return render(request,'seller/graph.html',context)

# Create your views here.
