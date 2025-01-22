from rest_framework.generics import ListAPIView ,RetrieveAPIView
from .models import Product
from .serializers import ProductListSerializer , ProductDetailSerializer
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

class ProductListView(ListAPIView):
    queryset = Product.objects.filter(stock__gt=0).select_related('category')
    serializer_class = ProductListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['category__id', 'price']  
    search_fields = ['name'] 

class ProductDetailView(RetrieveAPIView):
    queryset = Product.objects.filter(stock__gt=0).select_related('category')
    serializer_class = ProductDetailSerializer