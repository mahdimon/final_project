from rest_framework import serializers
from .models import Product ,Discount


class ProductListSerializer(serializers.ModelSerializer):
    discounted_price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'image', 'discounted_price','stock'] 

    def get_discounted_price(self, obj):
        discount :Discount= obj.discount
        if discount:
            if discount.discount_type == Discount.PERCENTAGE:
                max_discount = discount.max_discount if discount.max_discount is not None else float('inf')
                return obj.price - min((obj.price * discount.value / 100), max_discount)
            elif discount.discount_type == Discount.FIXED:
                return obj.price - discount.value
        return obj.price
        
class ProductDetailSerializer(ProductListSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)  

    class Meta(ProductListSerializer.Meta): 
        fields = ProductListSerializer.Meta.fields + ['brand', 'category_name']  