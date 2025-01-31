from rest_framework import serializers
from orders.models import Order, OrderProduct
from products.models import Product  



class OrderItemSerializer(serializers.ModelSerializer):
    product_image = serializers.SerializerMethodField()
    product_price = serializers.DecimalField(source="price", max_digits=13, decimal_places=2)
    quantity = serializers.IntegerField()

    class Meta:
        model = OrderProduct
        fields = ["product_image", "product_price", "quantity"]

    def get_product_image(self, obj):
        request = self.context.get("request") 
        if obj.product and obj.product.image:
            image_url = obj.product.image.url 
            return request.build_absolute_uri(image_url) if request else image_url  # Convert to full URL
        return None

class OrderHistorySerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(source="order_products", many=True)  
    total_paid = serializers.DecimalField(source="total_price", max_digits=15, decimal_places=2)
    status = serializers.SerializerMethodField()
  

    class Meta:
        model = Order
        fields = ["status", "total_paid", "items", "created_at"]
        
    def get_status(self, obj):
        return obj.get_status_display()
