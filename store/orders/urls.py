from django.urls import path
from .views import CheckoutView,VerifyPaymentAPIView


urlpatterns = [
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('verify/', VerifyPaymentAPIView.as_view(), name='verify'),

]
