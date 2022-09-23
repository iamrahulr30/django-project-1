from django.urls import path
from django.urls.resolvers import URLPattern
from .views import HomeView, Productview, Shopview
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.register, name='register'),
    # path('/',HomeView.as_view(),name='user-home')
    path('login/', auth_views.LoginView.as_view(template_name='user/login.html'), name="login"),
    path('', views.home, name='user-home'),
    path('logout/', auth_views.LogoutView.as_view(template_name='user/logout.html'), name="logout"),
    path('shops/', views.shops, name='shoppage'),
    path('mainshop/<int:shop>/', views.shopmain, name='shopmain'),
    path('mycart/', views.cart, name='user-cart'),
    path('profile/', views.profile, name='user-profile'),
    path('product_page/<int:pk>', views.pro_pg, name='propgu'),
    path('product_page/<int:pk>', Productview.as_view(), name='propg'),
    path('add_to_cart/<int:pk>', views.add_to_cart, name='add'),
    path('remove_from_cart/<int:pk>', views.remove_from_cart, name='remove'),
    path('purchase/<int:pk>', views.buy, name='buy'),
    path('purchase/', views.buy_cart, name='buycart'),
    path('updatetouser',views.userupdate,name='user-update'),
    path('myorders',views.userorders,name='user-orders')

]
