from django.shortcuts import get_object_or_404
from django.core.cache import cache
from django.conf import settings
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
import json
import requests
from .serializers import OrderHistorySerializer
from .models import Product, Coupon, Order, OrderProduct
from users.models import Address


class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]

    def calculate_prices(self, cart, coupon_code=None):
        """
        Calculate total and discounted prices for the given cart and coupon.
        """
        total_price = 0
        discounted_price = 0
        order_items = []

        for product_id, quantity in cart.items():
            product = get_object_or_404(Product, id=product_id)

            if product.stock < quantity:
                raise ValidationError(f"Not enough stock for {product.name}. Available: {product.stock}")

            item_price = product.price * quantity
            total_price += item_price
            discounted_price += (product.calculate_discounted_price() or product.price) * quantity  

            order_items.append({
                "product_id": product.id,  
                "quantity": quantity,
                "price": item_price
            })

        applied_coupon = None
        if coupon_code:
            try:
                applied_coupon = Coupon.objects.get(code=coupon_code)
            except Coupon.DoesNotExist:
                raise ValidationError("Invalid coupon code.")

            if not applied_coupon.is_valid():
                raise ValidationError("Expired coupon code.")

            discounted_price = applied_coupon.get_discounted_price(discounted_price)

        return total_price, discounted_price, order_items, applied_coupon

    def get(self, request):
        """
        Handle GET request to preview total price and discounted price before checkout.
        """
        cart = request.query_params.get("cart")
        coupon_code = request.query_params.get("coupon")

        if not cart:
            return Response({"error": "Cart data is required"}, status=400)

        try:
            cart = json.loads(cart)  # Convert string to dictionary safely
            total_price, discounted_price, _, _ = self.calculate_prices(cart, coupon_code)
            return Response({"total_price": total_price, "discounted_price": discounted_price})
        except Exception as e:
            return Response({"error": str(e)}, status=400)

    def post(self, request):
        """
        Handle POST request to create a pending order for later payment.
        """
        user = request.user
        cart = request.data.get("cart", {})
        coupon_code = request.data.get("coupon")
        address_id = request.data.get("address_id")

        address = get_object_or_404(Address, id=address_id, customer=user)

        try:
            total_price, discounted_price, order_items, applied_coupon = self.calculate_prices(cart, coupon_code)
        except ValidationError as e:
            return Response({"error": str(e)}, status=400)

        headers = {
            "accept": "application/json",
            "content-type": "application/json",
        }

        data = {
            "merchant_id": settings.ZARINPAL_MERCHANT_ID,
            "amount": int(discounted_price),  # Convert to int (ZarinPal requires Toman, not Decimal)
            "callback_url": settings.ZARINPAL_CALLBACK_URL,
            "description": "Online store purchase",
            "currency" : "IRT"
        }

        response = requests.post(settings.ZARINPAL_WEBSERVICE, json=data, headers=headers)
        result = response.json()

        if "data" in result and result["data"].get("code") == 100:
            authority = result["data"]["authority"]
            payment_url = f"{settings.ZARINPAL_STARTPAY_URL}{authority}"

            # Save order in cache for later processing after payment verification
            order_data = {
                "user_id": user.id,
                "order_items": order_items,
                "coupon_code": coupon_code,
                "address_id": address_id,
                "total_price": total_price,
                "discounted_price": discounted_price,
                "authority": authority  
                
            }
            
            cache.set(f"pending_order_{user.id}", order_data, timeout=3600)

            return Response({'payment_url': payment_url}, status=200)

        else:
            return Response({'error': "Cannot connect to ZarinPal"}, status=400)

class VerifyPaymentAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user 
        authority = request.query_params.get("Authority")
        payment_status = request.query_params.get("Status")
        print(payment_status)

        if payment_status != "OK":
            return Response({"error": "Transaction failed or canceled by user"}, status=400)
        
        
        cached_order = cache.get(f"pending_order_{user.id}")
        if not cached_order:
            return Response({"error": "Order not found or expired"}, status=400)
        if authority != cached_order["authority"]:
            return Response({"error": "wrong authority code"}, status=400)
        
        

        payload = {
            "merchant_id": settings.ZARINPAL_MERCHANT_ID,
            "amount": float(cached_order["discounted_price"]),  
            "authority": authority,
        }
        
        headers = {
            "accept": "application/json",
            "content-type": "application/json"
        }

        response = requests.post(settings.ZARINPAL_VERIFY_URL, json=payload, headers=headers)
        result = response.json()
     

        if result.get("data") and result["data"].get("code") == 100:
            # Payment was successful, finalize the order
            order = Order.objects.create(
                user=user,
                total_price=int(cached_order['discounted_price']))   
            
            if cached_order.get("coupon_code"):
                try:
                    coupon = Coupon.objects.get(code=cached_order["coupon_code"])
                    order.coupon = coupon
                    order.save()
                except Coupon.DoesNotExist:
                    pass 

            for item in cached_order["order_items"]:
                product = Product.objects.get(id=item["product_id"])
                OrderProduct.objects.create(
                    order=order,
                    product=product,
                    quantity=item["quantity"],
                    price=int(item["price"]/int(item["quantity"])),
                    prediscount_price=product.price,  

                )
           
            

            return Response(
                {"message": "Payment successful", "ref_id": result["data"]["ref_id"]},
                status=200
            )

        elif result.get("data") and result["data"].get("code") == 101:
            return Response(
                {"message": "Transaction already submitted"},
                status=200
            )

        else:
            print(result)
            return Response(
                {"error": "Transaction failed", "details": result},
                status=400
            )



class OrderHistoryView(ListAPIView):
    serializer_class = OrderHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related("order_products__product")

    def get_serializer_context(self):
        return {"request": self.request}  
