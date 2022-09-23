from user.views import pro_pg
from seller.models import Sellerprofile
from django.urls import path
from . import views
from .views import ProductUpdateView,OrderUpdateView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('sellerhome/',views.sellerhome,name="seller-home"),
    path('seller-profile/update/',views.SellerUpdate,name='seller-update'),
    path('productpg/<int:pk>',views.propage,name='seller-product'),
    path('Newproduct/',views.newproduct,name='newproduct'),
    path('productupdate/<int:pk>',ProductUpdateView.as_view(),name='productupdate'),
    path('orders/',views.sellerorder,name='seller-order'),
    path('OrderUpdateView/<int:pk>',OrderUpdateView.as_view(),name='orderupdate'),
    path('OrderDeleteView/<int:pk>',views.ordel,name='upgradeorder'),
    path('graphs/',views.sellergraph,name="seller-graph")
]
