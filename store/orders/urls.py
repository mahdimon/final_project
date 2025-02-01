from django.urls import path
from .views import CheckoutView, VerifyPaymentAPIView, OrderHistoryView


urlpatterns = [
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('verify/', VerifyPaymentAPIView.as_view(), name='verify'),
    path('history/', OrderHistoryView.as_view(), name='verify'),

]
