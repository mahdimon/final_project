from rest_framework.generics import ListAPIView ,RetrieveAPIView
from .models import Product ,Category
from .serializers import ProductListSerializer , ProductDetailSerializer,CategorySerializer, RecursiveCategorySerializer
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

class ProductListView(ListAPIView):
    queryset = Product.objects.filter(stock__gt=0).select_related('category')
    serializer_class = ProductListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    # filterset_fields = ['category__id', 'price']  
    filterset_fields = {
    'category__id': ['exact', 'in'],
    'price': ['exact', 'gte', 'lte'],
    }
    search_fields = ['name'] 

class ProductDetailView(RetrieveAPIView):
    queryset = Product.objects.filter(stock__gt=0).select_related('category')
    serializer_class = ProductDetailSerializer
    


class CategoryListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class NestedCategoryListView(ListAPIView):
    queryset = Category.objects.filter(parent=None)  
    serializer_class = RecursiveCategorySerializer