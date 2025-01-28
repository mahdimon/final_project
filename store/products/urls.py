from django.urls import path
from .views import ProductListView ,ProductDetailView,NestedCategoryListView


urlpatterns = [
    path('', ProductListView.as_view(), name='product-list'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('categories/', NestedCategoryListView.as_view(), name='nested-category-list')
]
