from django.db.models import fields
import django_filters
from django_filters import DateFilter,CharFilter
from seller.models import Product, Sellerprofile
from .models import order


class Productfilter(django_filters.FilterSet):
    title = CharFilter(field_name="title", lookup_expr='icontains')
    class Meta:
        model = Product
        fields = ['title', 'price','filter']



class OrderFilter(django_filters.FilterSet):
    customer = CharFilter(field_name="customer",lookup_expr="icontains")
    name = CharFilter(field_name="name",lookup_expr="icontains")
    start_date = DateFilter(field_name="date_time", lookup_expr='gte')
    end_date = DateFilter(field_name="date_time", lookup_expr='lte')

    class Meta:
        model = order
        fields = ['customer','name','date_time','delivered']

class shopfilter(django_filters.FilterSet):
    shop_name = CharFilter(field_name="shop_name", lookup_expr='icontains')

    class Meta:
        model = Sellerprofile
        fields = ['shop_name']
